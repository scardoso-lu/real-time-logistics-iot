Real-Time Logistics IoT Pipeline 🚛

This project demonstrates a full IoT-to-cloud pipeline for real-time vehicle detection and analytics using:
- Edge AI: Raspberry Pi + Hailo + DeGirum YOLO
- Messaging: MQTT (Mosquitto) for lightweight event streaming
- Cloud Analytics: Microsoft Fabric Event Streaming via Kafka
- Visualization: Optional Power BI dashboards

## Install and start Mosquitto

```
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

## Install AI detection
```
# Create virtual environment
python -m venv degirum
source degirum/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Pipeline

### Option 1: Single orchestrator (threads)
```
python app.py
```

### Option 2: Separate services

#### Terminal 1: Run edge detection
```
python detect.py
```
#### Terminal 2: Run Fabric publisher
```
python fabric.py
```