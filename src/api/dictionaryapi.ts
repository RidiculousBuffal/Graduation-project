import {fetchAPI} from "./index.ts";
import type {dictionaryType} from "../store/dictionary/type.ts";
import type {Pagination, PaginationResult} from "../publicTypes/pagination.ts";
import {clean} from "../publicTypes/typeUtils.ts";
import qs from "qs";

export const getDictionaryById = async (dictionaryId: string) => {
    return fetchAPI.req<dictionaryType>(`/dict/getDictionary/${dictionaryId}`, {method: "GET"})
}
export const getChildrenByParentId = async (parentId: string) => {
    return fetchAPI.req<dictionaryType[]>(`/dict/getChildrenByParentKey/${parentId}`, {method: "GET"})
}
export type SearchDictionaryPayload = {
    dict_name?: string,
    parent_key?: string
}
export const searchDictionary = async (request: SearchDictionaryPayload & Pagination) => {
    const {total, total_pages, ...rest} = request
    const payload = qs.stringify(clean(rest))
    return fetchAPI.req<PaginationResult<dictionaryType>>(`/dict/searchDictionary?${payload}`, {method: "GET"})
}