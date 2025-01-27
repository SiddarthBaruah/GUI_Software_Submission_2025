import paho.mqtt.client as mqtt

#MQTT Broker details
BROKER = "test.mosquitto.org"  #Broker URL
PORT = 1883  #Default MQTT port
TOPIC = "hyperloop/pod_data"

#Function to handle received messages
def on_message(client, userdata, msg):
    print(f"Received: {msg.payload.decode()}")

#Subscriber code
client = mqtt.Client("Subscriber", protocol=mqtt.MQTTv311)
client.connect(BROKER, PORT)

client.subscribe(TOPIC)
client.on_message = on_message

print("Subscriber connected to broker and waiting for messages...")
try:
    client.loop_forever()  #Keep listening for messages
except KeyboardInterrupt:
    print("Subscriber stopped.")
    client.disconnect()