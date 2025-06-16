import type {AircraftArrayType, AircraftImageType, aircraftType_, aircraftTypeType} from "../store/aircraft/types.ts";
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

export const createAircraft = async (aircraft: Partial<aircraftType_>) => {
    return fetchAPI.req<aircraftType_ & aircraftTypeType>('/aircraft/createAircraft', {
        method: "POST",
        body: JSON.stringify(aircraft)
    })
}
export const updateAircraft = async (aircraft: aircraftType_) => {
    return fetchAPI.req<aircraftType_ & aircraftTypeType>(`/aircraft/updateAircraft/${aircraft.aircraft_id}`, {
        method: "POST",
        body: JSON.stringify(aircraft)
    })
}
export const deleteAircraft = async (aircraft: aircraftType_) => {
    return fetchAPI.req<Boolean>(`/aircraft/deleteAircraft/${aircraft.aircraft_id}`, {method: "DELETE"})
}
export const searchAircraft = async (request: Pagination & Nullable<Omit<aircraftType_ & aircraftTypeType, 'aircraft_id' | 'typeid'>>) => {
    const {total, total_pages, ...rest} = request
    const payload = qs.stringify(clean(rest))
    return fetchAPI.req<PaginationResult<aircraftType_ & aircraftTypeType>>(`/aircraft/searchAircraft?${payload}`, {method: "GET"})
}

export const createAircraftImage = async (aircraftImage: Partial<AircraftImageType>) => {
    return fetchAPI.req<AircraftImageType>('/aircraft/createAircraftImage', {
        method: "POST",
        body: JSON.stringify(aircraftImage)
    })
}

export const getAircraftImage = async (imageId: string) => {
    return fetchAPI.req<AircraftImageType>(`/aircraft/getAircraftImage/${imageId}`, {method: "GET"})
}
export const updateAircraftImage = async (aircraftImage: AircraftImageType) => {
    return fetchAPI.req<AircraftImageType>(`/aircraft/updateAircraftImage/${aircraftImage.image_id}`, {
        method: "POST",
        body: JSON.stringify(aircraftImage)
    })
}
export const deleteAircraftImage = async (imageId: string) => {
    return fetchAPI.req<Boolean>(`/aircraft/deleteAircraftImage/${imageId}`, {method: "DELETE"})
}
export const searchAircraftImage = async (request: Pagination & {
    image_name?: string,
    aircraft_id?: string,
    aircraft_name?: string
}) => {
    const {total, total_pages, ...rest} = request
    const payload = qs.stringify(clean(rest))
    return fetchAPI.req<PaginationResult<AircraftImageType>>(`/aircraft/searchAircraftImage?${payload}`, {method: "GET"})
}