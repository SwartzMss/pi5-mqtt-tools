import json
import random
import time

import paho.mqtt.client as mqtt


class MQTTPublisher:
    """定时发布随机温度数据或自定义消息。"""

    def __init__(
        self,
        host: str,
        port: int,
        topic: str,
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


def start_publisher(host: str, port: int, topic: str, client: mqtt.Client) -> None:
    """兼容旧接口，按给定参数启动 ``MQTTPublisher``。"""
    MQTTPublisher(host=host, port=port, topic=topic, client=client).start()
