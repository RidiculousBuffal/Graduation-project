import type {EasySlice, MiddlewareTypes} from "@/store/baseType.ts";
import type {Log} from "@/store/log/types.ts";
import type {StateCreator} from "zustand/vanilla";
import type {LogState} from "@/store/log/logStore.ts";
import {initPagination} from "@/publicTypes/pagination.ts";

export type LogSlice = EasySlice<"log", Log, Log>
export const createLogSlice: StateCreator<LogState, MiddlewareTypes, [], LogSlice> = (setState, getState) => {
    return {
        logsPagination: initPagination,
        logs: [],
        setLogs: (logs) => {
            setState({
                ...getState,
                logs: logs
            })
        },
        updateLog: (log) => {
            const current = getState()
            const newLog = current.logs.map(x => {
                if (x.log_id == log.log_id) {
                    return log
                } else {
                    return x
                }
            })
            setState({
                ...getState(),
                logs: newLog
            })
        },
        setLogsPagination: (obj) => {
            setState({
                ...getState(),
                logsPagination: obj
            })
        },
    }
}