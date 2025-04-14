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
            url: process.env.ALCHEMY_SEPOLIA_URL,
            accounts: [process.env.SEPOLIA_PRIVATE_KEY!]
        }
    }
};

export default config;
