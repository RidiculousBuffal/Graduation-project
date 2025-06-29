#!/bin/sh

# 启动 hardhat node 到后台
npx hardhat node &

# 等待端口 8545 启动（可自定义时间或用 npx wait-port 之类的工具更优雅）
sleep 6

# 部署报名
npx hardhat ignition deploy ./ignition/modules/OperationLogger.ts --network hardhat

# 用 tail 阻塞，防止容器退出（可选，方便查看日志）
tail -f /dev/null