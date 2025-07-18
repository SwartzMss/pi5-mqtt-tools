import argparse

import paho.mqtt.client as mqtt

import publisher
import subscriber
from config import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_TOPIC


def main() -> None:
    parser = argparse.ArgumentParser(description="MQTT 发布/订阅示例")
    parser.add_argument(
        "mode",
        choices=["publish", "subscribe"],
        help="选择运行模式 (publish / subscribe)",
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help="MQTT Broker 地址")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="MQTT Broker 端口")
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help="MQTT 主题")
    parser.add_argument("--message", help="发布模式下要发送的消息")
    args = parser.parse_args()

    if args.mode == "publish":
        pub = publisher.MQTTPublisher(
            host=args.host, port=args.port, topic=args.topic, client=mqtt.Client()
        )
        pub.start(args.message)
    else:
        sub = subscriber.MQTTSubscriber(host=args.host, port=args.port, topic=args.topic)
        sub.start()


if __name__ == "__main__":
    main()
