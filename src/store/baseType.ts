import {immer} from 'zustand/middleware/immer'
import {persist} from "zustand/middleware/persist";
import {type Pagination} from "../publicTypes/pagination.ts";
// reference https://github.com/tauri-apps/tauri/discussions/6677
export type  MiddlewareTypes = [
    ['zustand/persist', unknown],
    ['zustand/immer', unknown]
]
type Capitalize<S extends string> = S extends `${infer F}${infer R}`
    ? `${Uppercase<F>}${R}`
    : S;


// 使用映射类型定义接口 since 0624
export type EasySlice<Name extends string, listType, originalType> = {
    [K in `${Name}s`]: listType[]
} & {
    [K in `set${Capitalize<Name>}s`]: (list: listType[]) => void
} & {
    [K in `update${Capitalize<Name>}`]: (obj: originalType) => void
} & {
    [K in `${Name}sPagination`]: Pagination
} & {
    [K in `set${Capitalize<Name>}sPagination`]: (pagination: Pagination) => void
};