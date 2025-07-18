import json
import random
import time

import paho.mqtt.client as mqtt

# 默认连接参数，可在实例化 ``MQTTPublisher`` 时覆盖
DEFAULT_HOST = "192.168.1.100"
DEFAULT_PORT = 1883
DEFAULT_TOPIC = "home/sensor/temperature"


class MQTTPublisher:
    """定时发布随机温度数据。"""

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        topic: str = DEFAULT_TOPIC,
        client: mqtt.Client | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.topic = topic
        self.client = client or mqtt.Client()

    def start(self) -> None:
        """连接到 Broker 并循环发布消息。"""
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()
        try:
            while True:
                temperature = round(random.uniform(20.0, 30.0), 2)
                payload = json.dumps({"temperature": temperature})
                self.client.publish(self.topic, payload)
                print(f"已发布 → {self.topic}: {payload}")
                time.sleep(5)
        except KeyboardInterrupt:
            pass
        finally:
            self.client.loop_stop()
            self.client.disconnect()


def start_publisher(client: mqtt.Client) -> None:
    """兼容旧接口，启动默认 ``MQTTPublisher``。"""
    MQTTPublisher(client=client).start()
