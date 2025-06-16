import type {terminalType} from "../store/terminal/types.ts";
import {fetchAPI} from "./index.ts";
import type {Pagination, PaginationResult} from "../publicTypes/pagination.ts";
import qs from 'qs'
import {clean, type Nullable} from "../publicTypes/typeUtils.ts";

export async function createTerminal(terminal: Omit<terminalType, 'terminal_id'>): Promise<terminalType | null> {
    return fetchAPI.req('/terminal/createTerminal', {method: "POST", body: JSON.stringify(terminal)})
}

export async function getTerminalDetailById(terminalId: string): Promise<terminalType | null> {
    return fetchAPI.req(`/terminal/getTerminal${terminalId}`, {method: "GET"})
}

export async function updateTerminal(terminal: terminalType): Promise<terminalType | null> {
    return fetchAPI.req(`/terminal/updateTerminal/${terminal.terminal_id}`, {
        method: "POST",
        body: JSON.stringify(terminal)
    })
}

export async function deleteTerminal(terminalId: string): Promise<boolean | null> {
    return fetchAPI.req(`/terminal/deleteTerminal/${terminalId}`, {method: "DELETE"})
}

export async function searchTerminal(request: Pagination & Nullable<Omit<terminalType, 'terminal_id'>>): Promise<PaginationResult<terminalType> | null> {
    const {total, total_pages, ...rest} = request
    const params = qs.stringify(clean(rest))
    return fetchAPI.req(`/terminal/searchTerminal?${params}`, {method: "GET"})
}