import cayenne.client
import time

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "f7f984b0-45c6-11ee-9ab8-d511caccfe8c"
MQTT_PASSWORD  = "0cd98ceb5ad9a82a4072e2797bcb0696c9dddac8"
MQTT_CLIENT_ID = "42e94170-45c9-11ee-8485-5b7d3ef089d0"

# The callback for when a message is received from Cayenne.
def on_message(message):
  print("message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise return nothing.

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883)

i=0
timestamp = 0

while True:
  client.loop()

  if (time.time() > timestamp + 10):
    client.celsiusWrite(1, i)
    client.luxWrite(2, i*10)
    client.hectoPascalWrite(3, i+800)
    timestamp = time.time()
    i = i+1