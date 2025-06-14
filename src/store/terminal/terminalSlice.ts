import type {terminalType} from "./types.ts";
import type {StateCreator} from "zustand/vanilla";
import type {TerminalState} from "./terminalStore.ts";
import type {MiddlewareTypes} from "../baseType.ts";
import {initPagination, type Pagination} from "../../publicTypes/pagination.ts";

export interface TerminalSlice {
    terminals: terminalType[]
    setTerminals: (terminals: terminalType[]) => void
    pagination: Pagination
    setPagination: (pagination: Pagination) => void
    updateTerminal: (terminal: terminalType) => void

}

export const createTerminalSlice: StateCreator<TerminalState, MiddlewareTypes, [], TerminalSlice> = (setState, getState, store) => {
    return {
        terminals: [],
        pagination: initPagination,
        setPagination: (pagination: Pagination) => {
            setState({...getState(), pagination: pagination})
        },
        setTerminals: (terminals: terminalType[]) => {
            setState({...getState(), terminals: terminals})
        },
        updateTerminal: (terminal: terminalType) => {
            const currentState = getState();
            const updatedTerminals = currentState.terminals.map(existingTerminal =>
                existingTerminal.terminal_id === terminal.terminal_id
                    ? terminal
                    : existingTerminal
            );
            setState({...currentState, terminals: updatedTerminals});
        }

    }
}