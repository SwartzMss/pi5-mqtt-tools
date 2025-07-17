import argparse

import paho.mqtt.client as mqtt

import publisher
import subscriber


def main() -> None:
    parser = argparse.ArgumentParser(description="MQTT 发布/订阅示例")
    parser.add_argument(
        "mode", choices=["publish", "subscribe"], help="选择运行模式 (publish / subscribe)"
    )
    args = parser.parse_args()

    if args.mode == "publish":
        client = mqtt.Client()
        publisher.start_publisher(client)
    else:
        subscriber.start_subscriber()


if __name__ == "__main__":
    main()
