import json

import paho.mqtt.client as mqtt

BROKER_HOST = "192.168.1.100"  # 改为你的 Broker IP 或域名
BROKER_PORT = 1883
TOPIC = "home/sensor/temperature"


def on_connect(client: mqtt.Client, userdata, flags, rc) -> None:
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage) -> None:
    try:
        data = json.loads(msg.payload.decode())
        print(f"[{msg.topic}] 收到消息：{data}")
    except json.JSONDecodeError:
        print(f"[{msg.topic}] 未能解析消息：{msg.payload}")


def start_subscriber() -> None:
    """Listen to MQTT topic and print received messages."""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_forever()
