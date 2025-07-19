# Raspberry Pi 5 MQTT 发布/订阅 系统部署指南

本项目示例演示如何在 **Raspberry Pi 5de (pi5de)** 上部署一个基于 `paho-mqtt` 的 MQTT 发布者（Publisher）和订阅者（Subscriber），用于温度数据的采集与联动。你可以在局域网内快速搭建轻量级消息系统，并结合 GPIO 控制实现自动化场景。

## 项目简介

本项目通过 Python 的 `paho-mqtt` 库，展示了如何在 Raspberry Pi 5de 上：

1. **订阅** MQTT 主题并打印或执行硬件联动（如风扇、LED）。
2. **发布** 自定义消息到 MQTT 主题，实现数据上报。

---

## 组件关系

本项目主要由两部分组成：

- **MQTT Broker（mosquitto）**：负责接收、存储和分发消息，是消息系统的核心服务器组件。
- **MQTT 客户端库（paho-mqtt）**：Eclipse Paho 提供的 Python 客户端库，用于在 Publisher 和 Subscriber 中实现与 Broker 的通信，支持消息的发布（publish）和订阅（subscribe）。

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

### 使用命令行测试 MQTT
```bash
# 订阅主题
mosquitto_sub -h 192.168.3.203 -p 1883 -t home/sensor/temperature
# 发布消息
mosquitto_pub -h 192.168.3.20 -p 1883 -t home/sensor/temperature \
              -m '{"temperature":27.5}'
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

### 5. 运行订阅者

```bash
python3 main.py subscribe --host 192.168.3.20 --port 1883 --topic home/sensor/temperature
```

日志示例：

```
Connected with result code 0
[home/sensor/temperature] 收到消息：25.34
```

### 6. 运行发布者

```bash
python3 main.py publish --host 192.168.3.20 --port 1883 --topic home/sensor/temperature --message '{"temperature": 27.5}'
```

---

## 进阶功能

1. **结构化 JSON 消息**：发送包含时间戳、传感器 ID 的 JSON 数据。
2. **QoS 与遗嘱消息**：提高可靠性，处理断线场景。
3. **GPIO 联动**：收到高温报警时控制风扇或 LED。\
   示例可在自定义回调函数中添加 GPIO 控制逻辑。

---


## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE)。

