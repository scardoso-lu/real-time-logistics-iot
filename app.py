import threading
from detect import edge_ai
from fabric import fabric_stream

if __name__ == "__main__":
    # Start detect.py (Edge → MQTT)
    detect_thread = threading.Thread(target=edge_ai, name="DetectThread")

    # Start fabric.py (MQTT → Kafka/Fabric)
    fabric_thread = threading.Thread(target=fabric_stream, name="FabricThread")

    # Start threads
    detect_thread.start()
    fabric_thread.start()

    # Wait for threads to finish (they run forever)
    detect_thread.join()
    fabric_thread.join()