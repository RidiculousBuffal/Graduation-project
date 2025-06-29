#!/bin/sh
npx hardhat node &
sleep 5
npx hardhat ignition deploy ./ignition/modules/OperationLogger.ts --network hardhat
tail -f /dev/null