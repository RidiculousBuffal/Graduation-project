import {expect} from "chai";
import {anyValue} from "@nomicfoundation/hardhat-chai-matchers/withArgs";
import hre from "hardhat";
import {OperationLogger} from "../typechain-types";
import {SignerWithAddress} from "@nomicfoundation/hardhat-ethers/signers";

describe("OperationLogger", function () {
    let contract: OperationLogger;
    let owner: SignerWithAddress;
    let otherAccount: SignerWithAddress;

    beforeEach(async function () {
        // 获取合约工厂和账户
        const OperationLogger = await hre.ethers.getContractFactory("OperationLogger");
        [owner, otherAccount] = await hre.ethers.getSigners();

        // 部署合约
        contract = await OperationLogger.deploy() as OperationLogger;
        await contract.waitForDeployment();
    });

    describe("Logging Operations", function () {
        it("should log operation and increase log count", async function () {
            // 初始日志总数应为 0
            expect(await contract.getLogCount()).to.equal(0);

            // 记录一条操作日志
            await contract.logOperation("Test Action 1");

            // 检查日志总数
            expect(await contract.getLogCount()).to.equal(1);
        });

        it("should store operation details in recentLogs", async function () {
            // 记录一条操作日志
            const action: string = "Test Action 2";
            await contract.connect(owner).logOperation(action);

            // 获取最近日志
            const logs = await contract.getRecentLogs();
            expect(logs.length).to.equal(1);
            expect(logs[0].operator).to.equal(owner.address);
            expect(logs[0].action).to.equal(action);
            // 检查时间戳大致正确（无法精确预测，但应接近当前时间）
            expect(logs[0].timestamp).to.be.gt(0);
        });

        it("should limit recentLogs to MAX_RECENT_LOGS", async function () {
            // 记录超过 MAX_RECENT_LOGS 的日志条目
            const limit_logs: number = 50;
            for (let i = 0; i < limit_logs; i++) {
                await contract.logOperation(`Action ${i}`);
            }
            // 检查日志总数
            expect(await contract.getLogCount()).to.equal(limit_logs);
            // 检查最近日志数量是否被限制为 MAX_RECENT_LOGS
            const logs = await contract.getRecentLogs();
            expect(logs.length).to.equal(limit_logs);
        });

        it("should emit OperationLogged event", async function () {
            const action: string = "Test Event";
            // 记录操作并监听事件
            await expect(contract.logOperation(action))
                .to.emit(contract, "OperationLogged")
                .withArgs(owner.address, anyValue, action, 0); // logId 应为 0（第一条日志）
        });
    });

    describe("Querying Logs", function () {
        beforeEach(async function () {
            // 预先记录一些日志以便查询
            await contract.logOperation("Query Action 1");
            await contract.connect(otherAccount).logOperation("Query Action 2");
        });

        it("should return correct log count", async function () {
            expect(await contract.getLogCount()).to.equal(2);
        });

        it("should retrieve specific log entry via getLogEntry", async function () {
            const [operator, timestamp, action]: [string, bigint, string] = await contract.getLogEntry(1);
            expect(operator).to.equal(otherAccount.address);
            expect(action).to.equal("Query Action 2");
            expect(timestamp).to.be.gt(0);
        });

        it("should revert if getLogEntry index is out of bounds", async function () {
            await expect(contract.getLogEntry(5)).to.be.revertedWith("Index out of bounds");
        });

        it("should return recent logs in correct order", async function () {
            const logs = await contract.getRecentLogs();
            expect(logs.length).to.equal(2);
            expect(logs[0].action).to.equal("Query Action 1");
            expect(logs[1].action).to.equal("Query Action 2");
        });
    });
});