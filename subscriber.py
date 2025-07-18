import json

import paho.mqtt.client as mqtt

from config import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_TOPIC


class MQTTSubscriber:
    """订阅指定主题并打印收到的消息。"""

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        topic: str = DEFAULT_TOPIC,
    ) -> None:
        self.host = host
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client: mqtt.Client, userdata, flags, rc) -> None:
        print(f"Connected with result code {rc}")
        client.subscribe(self.topic)

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage) -> None:
        try:
            data = json.loads(msg.payload.decode())
            print(f"[{msg.topic}] 收到消息：{data}")
        except json.JSONDecodeError:
            print(f"[{msg.topic}] 未能解析消息：{msg.payload}")

    def start(self) -> None:
        """连接到 Broker 并持续监听。"""
        self.client.connect(self.host, self.port, 60)
        self.client.loop_forever()


def start_subscriber() -> None:
    """兼容旧接口，启动默认 ``MQTTSubscriber``。"""
    MQTTSubscriber().start()
