import {fetchAPI} from "./index.ts";
import type {flightListType, flightType} from "../store/flight/types.ts";
import type {Pagination, PaginationResult} from "../publicTypes/pagination.ts";
import {clean, type Nullable} from "../publicTypes/typeUtils.ts";
import qs from "qs";

export type createFlightPayLoad = {
    aircraft_id: string,
    terminal_id?: string,
    estimated_departure: string, // ISO FORMAT with timezone
    estimated_arrival: string,
}
export const createFlight = async (payload: createFlightPayLoad) => {
    return fetchAPI.req<flightType>('/flight/createFlight', {method: "POST", body: JSON.stringify(payload)})
}
export const getFlightDetailById = async (flightId: string) => {
    return fetchAPI.req<flightType>(`/flight/getFlight/${flightId}`, {method: "GET"})
}
export const updateFlight = async (flight: flightType) => {
    return fetchAPI.req<flightType>(`/flight/updateFlight/${flight.flight_id}`, {
        method: "POST",
        body: JSON.stringify(flight)
    })
}
export const deleteFlight = async (flightId: string) => {
    return fetchAPI.req<boolean>(`/flight/deleteFlight/${flightId}`, {method: "DELETE"})
}
export type SearchFlightPayload = {
    flight_status?: string,
    health_status?: string,
    approval_status?: string,
    aircraft_name?: string,
    terminal_name?: string,
    estimated_departure_start?: string,
    estimated_departure_end?: string,
    estimated_arrival_start?: string,
    estimated_arrival_end?: string,
    actual_departure_start?: string,
    actual_departure_end?: string,
    actual_arrival_start?: string,
    actual_arrival_end?: string,
}
export const searchFlight = async (request: Pagination & Nullable<SearchFlightPayload>) => {
    const {total, total_pages, ...rest} = request
    const payload = qs.stringify(clean(rest))
    return fetchAPI.req<PaginationResult<flightListType>>(`/flight/searchFlight?${payload}`, {method: "GET"})
}