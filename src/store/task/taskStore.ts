import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {createTaskSlice, type TaskSlice} from "@/store/task/taskSlice.ts";

export type TaskState = TaskSlice

export const useTaskStore = create<TaskState>()(
    persist(
        immer(
            (...a) => ({
                ...createTaskSlice(...a)
            })
        ),
        {
            name: "Tasks",
            partialize: (state) => {
                return {
                    tasks: state.tasks
                }
            }
        }
    )
)