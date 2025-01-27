import paho.mqtt.client as mqtt
import time
import json
import random

#MQTT Broker details
BROKER = "test.mosquitto.org"  #Broker URL
PORT = 1883  #Default MQTT port
TOPIC = "hyperloop/pod_data"

#Other constants
PUBLISH_INTERVAL = 2  #seconds

battery = 100 #counter for battery level
#Simulated Pod data
def generate_pod_data():
    battery -= 1
    n = random.randint(0, 2) #randomly select a pod
    return {"pod_name": ["Avishkar-1", "Avishkar-2", "Avishkar-3"][n],
            "speed_kmph": [random.randint(100, 1200), 0, 0][n],
            "battery_level": battery,
            "status": ["Operational", "Maintenance", "Docked"][n]}

#Publisher code
client = mqtt.Client("Publisher", protocol=mqtt.MQTTv311)
client.connect(BROKER, PORT)

print("Publisher connected to broker")

#Publish data every <PUBLISH_INTERVAL> seconds
try:
    while True:
        pod_data = generate_pod_data()
        client.publish(TOPIC, json.dumps(pod_data))
        print(f"Published: {pod_data}")
        time.sleep(PUBLISH_INTERVAL)
except KeyboardInterrupt:
    print("Publisher stopped.")
    client.disconnect()