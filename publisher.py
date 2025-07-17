import json
import random
import time

import paho.mqtt.client as mqtt

BROKER_HOST = "192.168.1.100"  # 改为你的 Broker IP 或域名
BROKER_PORT = 1883
TOPIC = "home/sensor/temperature"


def start_publisher(client: mqtt.Client) -> None:
    """Publish random temperature data periodically."""
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()
    try:
        while True:
            temperature = round(random.uniform(20.0, 30.0), 2)
            payload = json.dumps({"temperature": temperature})
            client.publish(TOPIC, payload)
            print(f"已发布 → {TOPIC}: {payload}")
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()
