import paho.mqtt.client as mqtt
from random import randrange
import time

# Define the MQTT broker
mqttBroker = "mqtt.eclipseprojects.io"

# Initialize MQTT client for publishing with callback API version as this is the 2.0 version of paho-mqtt which requires specifying the callback API version
publisher_client = mqtt.Client (callback_api_version=2.0)
publisher_client.connect(mqttBroker)

# Initialize MQTT client for subscribing with callback API version as this is the 2.0 version of paho-mqtt which requires specifying the callback API version
subscriber_client = mqtt.Client( callback_api_version=2.0)

# Callback function to handle received messages
def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))

# Connect the subscriber client and set the callback
subscriber_client.connect(mqttBroker)
subscriber_client.subscribe("PODS")
subscriber_client.on_message = on_message

# Start the subscriber loop
subscriber_client.loop_start()

try:
    while True:
        # Publish random data to the "PODS" topic
        randNumber = randrange(100)
        publisher_client.publish("PODS", f"Pod1 Battery = {randNumber}")
        randNumber = randrange(100)
        publisher_client.publish("PODS",f"POD1 Speed = {randNumber}km/hr")
        publisher_client.publish("PODS",f"POD1 Status= Operational")
        time.sleep(10)  # Wait 10 seconds before publishing the next value
except KeyboardInterrupt:
    print("Stopping...")
    # Stop the subscriber loop
    subscriber_client.loop_stop()
