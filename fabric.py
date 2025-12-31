import os
import json
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from dotenv import load_dotenv

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()  # Reads .env file if present

CONNECTION_STRING = os.getenv("FABRIC_CONNECTION_STRING")
EVENT_HUB_NAME = os.getenv("FABRIC_EVENT_HUB")

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "vehicles/events")

# ----------------------------
# Extract namespace from connection string
# ----------------------------
try:
    namespace = CONNECTION_STRING.split("/")[2].split(".")[0]
except Exception:
    raise ValueError("Invalid FABRIC_CONNECTION_STRING format")

# ----------------------------
# Kafka producer
# ----------------------------
producer = KafkaProducer(
    bootstrap_servers=f"{namespace}.servicebus.windows.net:9093",
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    sasl_plain_username="$ConnectionString",
    sasl_plain_password=CONNECTION_STRING,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_to_kafka(event):
    producer.send(EVENT_HUB_NAME, event)
    producer.flush()

# ----------------------------
# MQTT callbacks
# ----------------------------
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    event = json.loads(msg.payload)
    send_to_kafka(event)

def fabric_stream():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    fabric_stream()