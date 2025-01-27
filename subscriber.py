import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"  # MQTT broker address
PORT = 1883                   # Default MQTT port
TOPIC = "hyperloop/pod/data"  # Topic to subscribe to

def on_connect(client, userdata, flags, reason_code, properties):
    """
    Callback when the client successfully connects to the broker. Subscribes to the specified topic upon connection.
    """
    print(f"Connected with reason code {reason_code}")
    client.subscribe(TOPIC)  # Subscribing to the topic

def on_message(client, userdata, msg):
    """
    Callback when a message is received on the subscribed topic. Decodes and displays the received message.
    """
    print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")

def subscribe_to_data():
    """
    Sets up the MQTT client, connects to the broker, and processes incoming messages.
    """
    # Creating an instance of the Client class (represents the MQTT client)
    client = mqtt.Client(client_id="Subscriber", protocol=mqtt.MQTTv5)
    # Attributes like `on_connect` and `on_message` are set to handle specific events
    # Assigning callback functions to handle connection and message events
    client.on_connect = on_connect
    client.on_message = on_message
    # Connecting to the MQTT broker
    client.connect(BROKER, PORT, 60)
    # Starts the network loop to continuously process incoming
    client.loop_forever()

#Subscribing to topic
subscribe_to_data()


