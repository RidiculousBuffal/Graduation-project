# 区块链部分

## 安装说明
```bash
    cp .env.example .env # 自己填写一下变量
    npm install
    npx hardhat compile
    #在第一个终端
    npx hardhat node
    #新开一个终端
    npx hardhat ignition deploy .\ignition\modules\OperationLogger.ts --network localhost
```