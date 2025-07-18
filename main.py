def publish_message(host: str, port: int, topic: str, message: str) -> None:
    """
    简单发布函数：连接、发布、断开
    """
    client = mqtt.Client()
    client.connect(host, port, keepalive=60)
    result = client.publish(topic, message)
    if result[0] == mqtt.MQTT_ERR_SUCCESS:
        print(f"已发布 → {topic}: {message}")
    else:
        print(f"发布失败，状态码：{result[0]}")
    client.disconnect()


def main() -> None:
    parser = argparse.ArgumentParser(description="MQTT 发布/订阅 CLI")
    parser.add_argument(
        "mode", choices=["publish", "subscribe"], help="运行模式"
    )
    parser.add_argument("--host", default="192.168.1.100", help="MQTT Broker 地址")
    parser.add_argument("--port", type=int, default=1883, help="MQTT Broker 端口")
    parser.add_argument("--topic", default="#", help="MQTT 主题，支持通配符")
    parser.add_argument("--message", help="发布模式下要发送的消息")
    args = parser.parse_args()

    if args.mode == "publish":
        if not args.message:
            parser.error("publish 模式需要 --message 参数")
        publish_message(args.host, args.port, args.topic, args.message)
    else:
        # 默认回调打印原始负载
        subscriber = MQTTSubscriber(
            host=args.host,
            port=args.port,
            callback=lambda t, p: print(f"订阅消息 → 主题: {t}, 负载: {p}")
        )
        subscriber.add_subscription(args.topic)
        try:
            subscriber.start()
            # 持续运行，直到手动中断
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            subscriber.stop()

if __name__ == "__main__":
    main()
