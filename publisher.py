import paho.mqtt.client as mqtt

# MQTT Broker details
BROKER = "test.mosquitto.org"  
PORT = 1883
TOPIC = "hyperloop/pod/data"

# Publish function
def publish_data():
    # Create an MQTT client
    client = mqtt.Client(client_id="Publisher", protocol=mqtt.MQTTv5)

    # Connect to the broker
    client.connect(host=BROKER, port=PORT, keepalive=60)

    # Publish sample data
    client.publish(topic=TOPIC, payload="Hyperloop pod data: Speed 120 km/h, Battery 85%", qos=1)

    # Disconnect after publishing
    client.disconnect()

# Call the function
publish_data()

