#!/bin/sh
npx hardhat node --network hardhat --hostname 0.0.0.0 --port 8545&
sleep 5
npx hardhat ignition deploy ./ignition/modules/OperationLogger.ts --network hardhat
tail -f /dev/null