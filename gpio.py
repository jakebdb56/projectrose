import time
import RPi.GPIO as GPIO
from rpi_lcd import LCD

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

lcd = LCD()

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
chan_list = (23,24)


x = 1

while x <= 3:
    GPIO.output(23, 1)
    GPIO.output(24, 0)
    lcd.text("Pin 23 off",1)
    lcd.text("Pin 24 on",2)
    time.sleep(5)
    GPIO.output(23, 0)
    GPIO.output(24, 1)
    lcd.text("Pin 23 on",1)
    lcd.text("Pin 24 off",2)
    time.sleep(5)
    x = x+1

GPIO.output(chan_list, 1)
print("all done, clean up")

GPIO.cleanup()
lcd.clear()