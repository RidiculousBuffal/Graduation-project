// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OperationLogger {
    struct LogEntry {
        address operator;      // 执行操作的地址
        uint256 timestamp;     // 操作时间戳
        string action;         // 操作描述
    }

    LogEntry[] public recentLogs;
    uint256 constant MAX_RECENT_LOGS = 50;
    uint256 public logCount;

    event OperationLogged(address indexed operator, uint256 indexed timestamp, string action, uint256 logId);

    function logOperation(string memory _action) public {
        uint256 currentTime = block.timestamp;
        address operator = msg.sender;
        logCount++;

        LogEntry memory newLog = LogEntry({
            operator: operator,
            timestamp: currentTime,
            action: _action
        });

        if (recentLogs.length >= MAX_RECENT_LOGS) {
            for (uint256 i = 0; i < recentLogs.length - 1; i++) {
                recentLogs[i] = recentLogs[i + 1];
            }
            recentLogs[recentLogs.length - 1] = newLog;
        } else {
            recentLogs.push(newLog);
        }

        emit OperationLogged(operator, currentTime, _action, logCount - 1);
    }

    function getLogCount() public view returns (uint256) {
        return logCount;
    }

    function getRecentLogs() public view returns (LogEntry[] memory) {
        return recentLogs;
    }

    function getLogEntry(uint256 _index) public view returns (address operator, uint256 timestamp, string memory action) {
        require(_index < recentLogs.length, "Index out of bounds");
        LogEntry memory entry = recentLogs[_index];
        return (entry.operator, entry.timestamp, entry.action);
    }
}