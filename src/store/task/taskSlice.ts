import type {TaskListType, TaskType} from "./types.ts";
import type {StateCreator} from "zustand/vanilla";
import type {EasySlice, MiddlewareTypes} from "../baseType.ts";
import type {TaskState} from "./taskStore.ts";
import {initPagination} from "../../publicTypes/pagination.ts";

export type TaskSlice = EasySlice<'task', TaskListType, TaskType>
export const createTaskSlice: StateCreator<TaskState, MiddlewareTypes, [], TaskSlice> = (setState, getState, store) => {
    return {
        tasks: [],
        tasksPagination: initPagination,
        setTasks: (list) => {
            setState({
                ...getState(),
                tasks: list
            })
        },
        updateTask: (task) => {
            const currentState = getState()
            const newList = currentState.tasks.map((x) => {
                if (x.task_id == task.task_id) {
                    return {
                        ...x,
                        ...task
                    }
                } else {
                    return x
                }
            })
            setState(
                {
                    ...currentState,
                    tasks: newList
                }
            )
        },
        setTasksPagination: (pagination) => {
            setState({
                ...getState(),
                tasksPagination: pagination
            })
        }
    }
}