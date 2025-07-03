import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {createLogSlice, type LogSlice} from "@/store/log/logSlice.ts";

export type LogState = LogSlice
export const useLogStore = create<LogState>()(
    persist(
        immer((...a) => {
            return {
                ...createLogSlice(...a)
            }
        }),
        {
            name: "logStore",
            partialize: (state) => {
                return {
                    logs: state.logs
                }
            }
        }
    )
)