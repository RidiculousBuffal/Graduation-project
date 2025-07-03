import {fetchAPI} from "@/api/index.ts";
import type {Pagination, PaginationResult} from "@/publicTypes/pagination.ts";
import {clean} from "@/publicTypes/typeUtils.ts";
import qs from "qs";
import type {Log} from "@/store/log/types.ts";

export type blockChainStatus = {
    abi: any
    address: string
    url: string,
    status: string
}
export const getBlockChainStatus = async () => {
    return fetchAPI.req<blockChainStatus>('/log/blockChainStatus', {method: "GET"})
}
export const searchAuditLog = async (request: Pagination) => {
    const {total, total_pages, ...res} = request
    const payload = qs.stringify(clean(res))
    return fetchAPI.req<PaginationResult<Log>>(`/log/searchAuditLog?${payload}`, {method: "GET"})
}