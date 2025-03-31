#!/bin/bash

# 加载环境变量 `/etc/profile`
source /etc/profile

# 启动 FISCO-BCOS 节点
cd /root/fisco/nodes/127.0.0.1 && bash start_all.sh

# 启动 WeBASE-Front 服务
cd /root/fisco/webase-front && bash start.sh

# 保持容器运行
tail -f /dev/null