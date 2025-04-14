# 区块链部分

## 安装说明
```bash
    cp .env.example .env # 自己填写一下变量
    npm install
    npx hardhat compile
    npx hardhat test
    npx hardhat ignition deploy .\ignition\modules\OperationLogger.ts --network localhost
```