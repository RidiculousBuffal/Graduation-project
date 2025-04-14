// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const OperationLoggerModule = buildModule("OperationLoggerModule", (m) => {
  // 部署 OperationLogger 合约
  const operationLogger = m.contract("OperationLogger");

  return { operationLogger };
});

export default OperationLoggerModule;