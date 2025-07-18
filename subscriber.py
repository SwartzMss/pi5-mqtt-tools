import json
import paho.mqtt.client as mqtt
from typing import Callable, Optional, Set

class MQTTSubscriber:
    """
    灵活的 MQTT 订阅器：
    - 初始化时仅配置 Broker 地址、端口和消息回调
    - 提供 add_subscription()/remove_subscription() 动态管理主题
    - 调用 start() 建立连接并开始接收消息
    - 调用 stop() 停止并断开连接

    :param host: MQTT Broker 地址
    :param port: MQTT Broker 端口，默认 1883
    :param callback: 接收到消息后的处理函数，签名为 fn(topic: str, payload: bytes)
    :param client_id: 可选 client_id
    """
    def __init__(
        self,
        host: str,
        port: int = 1883,
        callback: Optional[Callable[[str, bytes], None]] = None,
        client_id: Optional[str] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.callback = callback or self._default_callback
        self.client = mqtt.Client(client_id=client_id) if client_id else mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self._is_connected = False
        self._topics: Set[str] = set()

    def _on_connect(self, client: mqtt.Client, userdata, flags, rc) -> None:
        if rc == 0:
            print(f"已连接 → {self.host}:{self.port}")
            # 连接后订阅所有已添加的主题
            for topic in self._topics:
                client.subscribe(topic)
                print(f"已订阅 → {topic}")
        else:
            print(f"连接失败，返回码：{rc}")

    def _on_message(
        self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage
    ) -> None:
        self.callback(msg.topic, msg.payload)

    @staticmethod
    def _default_callback(topic: str, payload: bytes) -> None:
        text = payload.decode(errors='ignore')
        try:
            data = json.loads(text)
            print(f"[{topic}] 收到消息：{data}")
        except json.JSONDecodeError:
            print(f"[{topic}] 收到消息（非 JSON）：{text}")

    def add_subscription(self, topic: str, qos: int = 0) -> None:
        """
        添加订阅主题；如果已连接则立即订阅。
        :param topic: 要订阅的主题
        :param qos: QoS 等级，默认 0
        """
        if topic not in self._topics:
            self._topics.add(topic)
            if self._is_connected:
                self.client.subscribe(topic, qos)
                print(f"已订阅 → {topic}")
        else:
            print(f"主题已存在：{topic}")

    def remove_subscription(self, topic: str) -> None:
        """
        移除订阅主题；如果已连接则取消订阅。
        :param topic: 要取消订阅的主题
        """
        if topic in self._topics:
            self._topics.remove(topic)
            if self._is_connected:
                self.client.unsubscribe(topic)
                print(f"已取消订阅 → {topic}")
        else:
            print(f"主题不存在：{topic}")

    def start(self, keepalive: int = 60) -> None:
        """
        连接到 MQTT Broker 并启动网络循环，开始接收消息。
        """
        if not self._is_connected:
            self.client.connect(self.host, self.port, keepalive)
            self.client.loop_start()
            self._is_connected = True
            print("启动监听...")
        else:
            print("已处于连接状态，无需重复连接")

    def stop(self) -> None:
        """
        停止网络循环并断开与 Broker 的连接。
        """
        if self._is_connected:
            self.client.loop_stop()
            self.client.disconnect()
            self._is_connected = False
            print("已断开连接")
        else:
            print("当前未连接，无需断开")
