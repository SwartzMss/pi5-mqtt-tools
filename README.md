# Raspberry Pi 5de MQTT 发布/订阅 系统部署指南

本项目示例演示如何在 **Raspberry Pi 5de (pi5de)** 上部署一个基于 `paho-mqtt` 的 MQTT 发布者（Publisher）和订阅者（Subscriber），用于温度数据的采集与联动。你可以在局域网内快速搭建轻量级消息系统，并结合 GPIO 控制实现自动化场景。

## 目录

- [项目简介](#项目简介)
- [组件关系](#组件关系)
- [示例代码](#示例代码)
- [部署步骤](#部署步骤)
- [进阶功能](#进阶功能)
- [许可证](#许可证)

---

## 项目简介

本项目通过 Python 的 `paho-mqtt` 库，展示了如何在 Raspberry Pi 5de 上：

1. **订阅** 温度主题并打印或执行硬件联动（如风扇、LED）。
2. **发布** 模拟温度数据到 MQTT 主题，实现数据上报。

---

## 组件关系

本项目主要由两部分组成：

- **MQTT Broker（mosquitto）**：负责接收、存储和分发消息，是消息系统的核心服务器组件。
- **MQTT 客户端库（paho-mqtt）**：Eclipse Paho 提供的 Python 客户端库，用于在 Publisher 和 Subscriber 中实现与 Broker 的通信，支持消息的发布（publish）和订阅（subscribe）。

---
## 示例代码

仓库提供 `main.py` 作为入口文件，通过命令行参数选择发布（publish）或订阅（subscribe）模式，内部调用 `publisher.py` 或 `subscriber.py` 实现逻辑。

```python
parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["publish", "subscribe"])
args = parser.parse_args()
```

根据参数决定调用 `publisher.start_publisher()` 或 `subscriber.start_subscriber()`。

```python
if args.mode == "publish":
    publisher.start_publisher(mqtt.Client())
else:
    subscriber.start_subscriber()
```

`start_publisher()` 主要逻辑：

```python
import json
import time
import random
import paho.mqtt.client as mqtt

client = mqtt.Client()

while True:
    temperature = round(random.uniform(20.0, 30.0), 2)
    payload = json.dumps({"temperature": temperature})
    client.publish(TOPIC, payload)
    time.sleep(5)
```

`start_subscriber()` 主要逻辑：

```python
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"[{msg.topic}] 收到消息：{data}")
```

## 部署步骤

### 1. 系统更新

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. 安装 Mosquitto Broker

```bash
sudo apt install mosquitto mosquitto-clients -y
sudo systemctl enable --now mosquitto
```

### 3. 安装 Python 依赖

```bash
sudo apt install python3-pip -y
pip3 install paho-mqtt
```

### 4. 获取代码

```bash
# 克隆或下载本仓库
git clone https://github.com/yourusername/pi5-mqtt-tools.git
cd pi5-mqtt-tools
```

### 5. 配置 Broker 地址

编辑 `publisher.py` 和 `subscriber.py` 中的连接参数：

```python
BROKER_HOST = "192.168.1.100"  # 改为你的 Broker IP 或域名
BROKER_PORT = 1883
TOPIC = "home/sensor/temperature"
```

### 6. 运行订阅者

```bash
python3 main.py subscribe
```

日志示例：

```
Connected with result code 0
[home/sensor/temperature] 收到消息：25.34
```

### 7. 运行发布者

```bash
python3 main.py publish
```

每隔 5 秒发布一次模拟温度：

```
已发布 → home/sensor/temperature: 27.81
```

---

## 进阶功能

1. **结构化 JSON 消息**：发送包含时间戳、传感器 ID 的 JSON 数据。
2. **QoS 与遗嘱消息**：提高可靠性，处理断线场景。
3. **GPIO 联动**：收到高温报警时控制风扇或 LED。\
   示例可在 `start_subscriber()` 函数中添加 GPIO 控制逻辑。

---


## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE)。

