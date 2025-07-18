import json
import random
import time

import paho.mqtt.client as mqtt

from config import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_TOPIC


class MQTTPublisher:
    """定时发布随机温度数据或自定义消息。"""

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

    def start(self, message: str | None = None) -> None:
        """连接到 Broker 并发送消息。"""
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()
        try:
            if message is not None:
                self.client.publish(self.topic, message)
                print(f"已发布 → {self.topic}: {message}")
            else:
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
