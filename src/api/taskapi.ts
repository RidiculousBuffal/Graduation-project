import {fetchAPI} from "./index.ts";
import type {TaskListType, TaskType} from "../store/task/types.ts";
import type {Pagination, PaginationResult} from "../publicTypes/pagination.ts";
import qs from "qs";
import {clean} from "../publicTypes/typeUtils.ts";

export type createTaskPayload = {
    flight_id: string,
    estimated_start: string,
    estimated_end: string,
}
export const createTask = async (task: createTaskPayload) => {
    return fetchAPI.req<TaskType>('/task/create', {
        method: "POST",
        body: JSON.stringify(task)
    })
}
export const getTaskById = async (taskId: string) => {
    return fetchAPI.req<TaskType>(`/task/getTaskById/${taskId}`, {method: "GET"})
}
export type updateTaskPayload = {
    task_id: string,
    flight_id: string,
    estimated_start: string,
    estimated_end: string,
    actual_start: string,
    actual_end: string,
    task_status: string,
}
export const updateTask = async (task: updateTaskPayload) => {
    return fetchAPI.req<TaskType>(`/task/updateTask/${task.task_id}`, {
        body: JSON.stringify(task),
        method: "PUT"
    })
}
export const deleteTask = async (taskId: string) => {
    return fetchAPI.req<boolean>(`/task/deleteTask/${taskId}`, {method: "DELETE"})
}
export type SearchTaskPayload = {
    flight_id?: string,
    admin_id?: string,
    task_status?: string,
    aircraft_id?: string,
    aircraft_name?: string,
    admin_name?: string,
    estimated_start_from?: string,
    estimated_start_to?: string,
    estimated_end_from?: string,
    estimated_end_to?: string,
    actual_start_from?: string,
    actual_start_to?: string,
    actual_end_to?: string,
    actual_end_from?: string
}
export const searchTask = async (request: SearchTaskPayload & Pagination) => {
    const {total, total_pages, ...rest} = request
    const payload = qs.stringify(clean(rest))
    return fetchAPI.req<PaginationResult<TaskListType>>(`/task/search?${payload}`, {method: "GET"})
}