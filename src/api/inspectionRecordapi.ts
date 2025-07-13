import type {InspectionRecordListType, InspectionRecordType} from "@/store/inspection/types.ts";
import {fetchAPI} from "@/api/index.ts";
import type {Pagination, PaginationResult} from "@/publicTypes/pagination.ts";
import {clean} from "@/publicTypes/typeUtils.ts";
import qs from "qs";

export type createInspectionRecordPayload = {
    inspection_name: string,
    executor_id: string,
    reference_image_id: string,
    task_id: string
}
export const createInspectionRecord = async (payload: createInspectionRecordPayload) => {
    return fetchAPI.req<InspectionRecordType>('/inspection/create', {
        method: "POST",
        body: JSON.stringify(payload)
    })
}
export const getInspectionRecordById = async (inspectionId: string) => {
    return fetchAPI.req<InspectionRecordListType>(`/inspection/getInspectionById/${inspectionId}`, {method: "GET"})
}
export type updateInspectionRecordPayload = {
    inspection_id?: string,
    inspection_name?: string,
    executor_id?: string,
    // reference_image_id?: string, 项目初期暂不支持更换底图这种操作
    task_id?: string,
    inspection_status?: string,
}
export const updateInspectionRecord = async (inspection: updateInspectionRecordPayload) => {
    return fetchAPI.req<InspectionRecordType>(`/inspection/updateInspection/${inspection.inspection_id}`, {
        method: "PUT",
        body: JSON.stringify(inspection)
    })
}
export const deleteInspectionRecord = async (inspectionId: string) => {
    return fetchAPI.req<boolean>(`/inspection/deleteInspection/${inspectionId}`, {method: "DELETE"})
}
export type SearchInspectionRecordPayload = {
    task_id?: string,
    executor_id?: string,
    inspection_status?: string,
    reference_image_id?: string,
    flight_id?: string,
    aircraft_id?: string,
    executor_name?: string,
    start_time_from?: string,
    start_time_to?: string,
    end_time_from?: string,
    end_time_to?: string,
}
export const searchInspectionRecords = async (request: SearchInspectionRecordPayload & Pagination) => {
    const {total, total_pages, ...rest} = request
    const payload = qs.stringify(clean(rest))
    return fetchAPI.req<PaginationResult<InspectionRecordListType>>(`/inspection/search?${payload}`, {method: "GET"})
}
export const searchMyInspectionRecords = async (request: SearchInspectionRecordPayload & Pagination) => {
    const {total, total_pages, ...rest} = request
    const payload = qs.stringify(clean(rest))
    return fetchAPI.req<PaginationResult<InspectionRecordListType>>(`/inspection/getMyInspections?${payload}`, {method: "GET"})
}