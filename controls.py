# compilation of shit for the soil sensor, display, and relay module

import time
import RPi.GPIO as GPIO
from rpi_lcd import LCD
import smbus
import decimal
import bme680

def temp():
# Get I2C bus
    bus = smbus.SMBus(1)

# SHT30 address, 0x44(68)
# Send measurement command, 0x2C(44)
#		0x06(06)	High repeatability measurement
    bus.write_i2c_block_data(0x44, 0x2C, [0x06])

    time.sleep(1)

# SHT30 address, 0x44(68)
# Read data back from 0x00(00), 6 bytes
# cTemp MSB, cTemp LSB, cTemp CRC, Humididty MSB, Humidity LSB, Humidity CRC
    data = bus.read_i2c_block_data(0x44, 0x00, 6)

# Convert the data
    cTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    fTemp = cTemp * 1.8 + 32
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    
# round for simpliicty    
    fTempround = round(fTemp)
    humidityround = int(humidity)
    return fTempround, humidityround


# establish time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

# establish LCD
lcd = LCD()

# GPIO pin setup for relay control
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
chan_list = (23,24)

# bme680 sensor inits

airq = bme680.BME680()

airq.set_humidity_oversample(bme680.OS_2X)
airq.set_pressure_oversample(bme680.OS_4X)
airq.set_temperature_oversample(bme680.OS_8X)
airq.set_filter(bme680.FILTER_SIZE_3)
airq.tempf = round((airq.data.temperature * 1.8) + 32)
airq.humid = round(airq.data.humidity)
airq.press = round(airq.data.pressure)
airq.presskpa = airq.press / 10

airq.set_gas_status(bme680.ENABLE_GAS_MEAS)
airq.set_gas_heater_temperature(320)
airq.set_gas_heater_duration(150)
airq.select_gas_heater_profile(0)
airq.gas = round(airq.data.gas_resistance)

# test settings
rhset = 65
ftempset = 75

# functions

# test gpio function loop
#while x <= 3:
#    GPIO.output(23, 1)
#    GPIO.output(24, 0)
#    lcd.text("Pin 23 off",1)
#    lcd.text("Pin 24 on",2)
#    time.sleep(5)
#    GPIO.output(23, 0)
#    GPIO.output(24, 1)
#    lcd.text("Pin 23 on",1)
#    lcd.text("Pin 24 off",2)
#    time.sleep(5)
#    x = x+1

temptxt = "Temp {}*F"
humidtxt = "RH {}%"

while 0 < 1:
    degf = temp()
    print("Temp ", degf[0],"*F")
    lcd.text(temptxt.format(degf[0]),1)
    print("RH ", degf[1],"%")
    lcd.text(humidtxt.format(degf[1]),2)
    #inserting bme sensor print
    print("Ambient temp ",airq.tempf,"*F")
    print("Relative Humidity ",airq.humid,"%")
    print("Baro Press.",airq.press,"mbar")
    print(airq.gas)
    time.sleep(.5)
else:
    lcd.text("Stop")

# cleanup
GPIO.output(chan_list, 1)
print("all done, clean up")

GPIO.cleanup()
lcd.clear()