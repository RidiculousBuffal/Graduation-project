import type {aircraftTypeType} from "../store/aircraft/types.ts";
import {fetchAPI} from "./index.ts";
import qs from "qs";
import {clean, type Nullable} from "../publicTypes/typeUtils.ts";
import type {Pagination, PaginationResult} from "../publicTypes/pagination.ts";

export const createAircraftType = async (aircraftType: Partial<aircraftTypeType>) => {
    return fetchAPI.req<aircraftTypeType>('/aircraft/createAircraftType', {
        method: "POST",
        body: JSON.stringify(aircraftType)
    })
}
export const getAircraftType = async (aircraftTypeId: string) => {
    return fetchAPI.req<aircraftTypeType>(`/aircraft/getAircraftType/${aircraftTypeId}`, {method: "GET"})
}
export const updateAircraftType = async (aircraftType: aircraftTypeType) => {
    return fetchAPI.req<aircraftTypeType>(`/aircraft/updateAircraftType/${aircraftType.typeid}`, {
        method: "POST",
        body: JSON.stringify(aircraftType)
    })
}
export const deleteAircraftType = async (aircraftTypeId: string) => {
    return fetchAPI.req<boolean>(`/aircraft/deleteAircraftType/${aircraftTypeId}`, {method: "DELETE"})
}

export const searchAircraftType = async (request: Pagination & Nullable<Omit<aircraftTypeType, 'typeid'>>) => {
    const {total, total_pages, ...rest} = request
    const payload = qs.stringify(clean(rest))
    return fetchAPI.req<PaginationResult<aircraftTypeType>>(`/aircraft/searchAircraftType?${payload}`, {method: "GET"})
}