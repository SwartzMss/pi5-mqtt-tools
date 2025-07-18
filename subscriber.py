import json

import paho.mqtt.client as mqtt


class MQTTSubscriber:
    """订阅指定主题并打印收到的消息。"""

    def __init__(
        self,
        host: str,
        port: int,
        topic: str,
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


def start_subscriber(host: str, port: int, topic: str) -> None:
    """兼容旧接口，按给定参数启动 ``MQTTSubscriber``。"""
    MQTTSubscriber(host=host, port=port, topic=topic).start()
