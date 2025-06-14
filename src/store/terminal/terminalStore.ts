import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {createTerminalSlice, type TerminalSlice} from "./terminalSlice.ts";

export type TerminalState = TerminalSlice
export const useTerminalStore = create<TerminalState>()(
    persist(
        immer(
            (...a) => ({
                ...createTerminalSlice(...a)
            })
        ),
        {
            name: 'terminalStore',
            partialize: (state) => {
                return {
                    terminals: state.terminals,
                }
            }
        }
    )
)