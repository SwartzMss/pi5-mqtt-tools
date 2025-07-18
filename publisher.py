import json
import paho.mqtt.client as mqtt

class MQTTPublisher:
    """
    简单的 MQTT 发布器：
    - 初始化时配置 Broker 地址、端口和可选 client_id
    - 调用 start() 建立连接、调用 publish() 发布消息、调用 stop() 断开
    """
    def __init__(self, host: str, port: int = 1883, client_id: str | None = None) -> None:
        self.host = host
        self.port = port
        self.client = mqtt.Client(client_id=client_id) if client_id else mqtt.Client()
        self._is_connected = False

    def start(self, keepalive: int = 60) -> None:
        """
        连接到 MQTT Broker 并启动网络循环。
        """
        if not self._is_connected:
            self.client.connect(self.host, self.port, keepalive)
            self.client.loop_start()
            self._is_connected = True
            print(f"已连接 → {self.host}:{self.port}")
        else:
            print("已处于连接状态，无需重复连接")

    def publish(
        self,
        topic: str,
        message: str | dict,
        qos: int = 0,
        retain: bool = True,
    ) -> None:
        """
        发布消息，需先调用 start() 建立连接。
        :param topic: 发布主题
        :param message: 字符串或字典（自动转换为 JSON）
        :param qos: MQTT QoS 等级
        :param retain: 是否保留消息
        """
        if not self._is_connected:
            raise RuntimeError("发布前请先调用 start() 方法连接到 Broker")
        payload = json.dumps(message) if isinstance(message, dict) else message
        result = self.client.publish(topic, payload, qos=qos, retain=retain)
        status = result[0]
        if status == mqtt.MQTT_ERR_SUCCESS:
            print(f"已发布 → {topic}: {payload}")
        else:
            print(f"发布失败，状态码：{status}")

    def stop(self) -> None:
        """
        停止网络循环并断开与 Broker 的连接。
        """
        if self._is_connected:
            self.client.loop_stop()
            self.client.disconnect()
            self._is_connected = False
            print(f"已断开 → {self.host}:{self.port}")
        else:
            print("当前未连接，无需断开")
