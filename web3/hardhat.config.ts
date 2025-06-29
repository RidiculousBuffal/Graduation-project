import {HardhatUserConfig} from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import 'dotenv/config'

const config: HardhatUserConfig = {
    solidity: "0.8.28",
    defaultNetwork: "hardhat",
    networks: {
        hardhat: {
            gas: 30000000, // 增加 gas 限制到 50,000,000
            gasPrice: 875000000, // 可选：调整 gas 价格
        },
        sepolia: {
            url: process.env.ALCHEMY_SEPOLIA_URL??"http://localhost:8545",
            accounts: [process.env.SEPOLIA_PRIVATE_KEY??"5267f2103eab089b87b113e3ce8d2489dc417f92e74e87455321584d44512eda"]
        }
    }
};

export default config;
