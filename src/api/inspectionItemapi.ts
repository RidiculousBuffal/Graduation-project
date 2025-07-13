import type {InspectionItemPoint} from "@/store/inspectionItem/types"
import {fetchAPI} from "@/api/index.ts";
import type {InspectionItem} from "@/store/inspectionItem/types";
import type {Pagination, PaginationResult} from "@/publicTypes/pagination.ts";
import qs from "qs";

export type createInspectionItemType = {
    item_name?: string,
    inspection_id: string,
    item_point: InspectionItemPoint,
    description?: string
    model_id: string,
}
export type updateInspectionItemType = createInspectionItemType
export const createInspectionItem = async (inspectionItem: createInspectionItemType) => {
    return fetchAPI.req<InspectionItem>('/inspection_item/create', {
        method: "POST",
        body: JSON.stringify(inspectionItem),
    })
}

export const getInspectionItemById = async (id: string) => {
    return fetchAPI.req<InspectionItem>(`/inspection_item/getItemById/${id}`, {method: "GET"})
}
export const updateInspectionItem = async (id: string, inspectionItem: updateInspectionItemType) => {
    return fetchAPI.req<InspectionItem>(`/inspection_item/updateItem/${id}`, {
        method: "PUT",
        body: JSON.stringify(inspectionItem),
    })
}
export const deleteInspectionItem = async (id: string) => {
    return fetchAPI.req<boolean>(`/inspection_item/deleteItem/${id}`, {method: "DELETE"})
}
export const searchInspectionItem = async (request: Pagination & { inspection_id: string }) => {
    const {total, total_pages, ...rest} = request
    const payload = qs.stringify(rest)
    return fetchAPI.req<PaginationResult<InspectionItem>>(`/inspection_item/listByInspection?${payload}`, {method: "GET"})
}
