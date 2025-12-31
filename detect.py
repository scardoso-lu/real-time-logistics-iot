import degirum as dg
import degirum_tools as dgt
import cv2
import paho.mqtt.client as mqtt
import json
import datetime
import os
from dotenv import load_dotenv

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()  # Reads .env file if present

DEVICE_ID = os.getenv("DEVICE_ID", "raspi-01")
BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", "vehicles/events")

SOURCE_PATH = os.getenv("SOURCE_PATH", "video")

MODEL_NAME = os.getenv("MODEL_NAME", "yolo11n_coco--640x640_quant_hailort_multidevice_1")
CONF_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.4))
ZOO_URL = os.getenv("ZOO_URL", "degirum/hailo")
HOST_ADDRESS = os.getenv("HOST_ADDRESS", "@local")

# ----------------------------
# MQTT setup
# ----------------------------
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

model = dg.load_model(
    model_name=MODEL_NAME,
    inference_host_address=HOST_ADDRESS,
    zoo_url=ZOO_URL,
)

# Overlay settings for debugging
model.overlay_show_labels = True
model.overlay_show_confidence = True
model.overlay_show_probabilities = True
model.overlay_show_bbox = True
model.confidence_threshold = CONF_THRESHOLD

# ----------------------------
# Detection loop
# ----------------------------
def edge_ai():
    with dgt.open_video_stream(SOURCE_PATH) as stream:
        for frame_id, result in enumerate(dgt.predict_stream(model, stream)):

            vehicles_detected = []

            for det in result.results:
                if len(det) > 0:
                    vehicles_detected.append({
                        "category_id": det["category_id"],
                        "label": det["label"],
                        "score": det["score"]
                    })

            # Publish only if there are detections
            if vehicles_detected:
                event = {
                    "device_id": DEVICE_ID,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "detections": vehicles_detected
                }
                
                client.publish(TOPIC, json.dumps(event))

            # Display overlay
            cv2.imshow("Inference", result.image_overlay)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    edge_ai()
