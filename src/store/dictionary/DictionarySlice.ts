import type {dictionaryType} from "./type.ts";
import {initPagination, type Pagination} from "../../publicTypes/pagination.ts";
import type {StateCreator} from "zustand/vanilla";
import type {DictionaryState} from "./DictionaryStore.ts";
import type {MiddlewareTypes} from "../baseType.ts";

export interface DictionarySlice {
    dictionaries: dictionaryType[]
    setDictionaries: (dictionaries: dictionaryType[]) => void
    dictPagination: Pagination
    setDictPagination: (pagination: Pagination) => void
}

export const createDictionarySlice: StateCreator<DictionaryState, MiddlewareTypes, [], DictionarySlice> = (setState, getState, store) => {
    return {
        dictionaries: [],
        setDictionaries: (dictionaries) => {
            return setState({...getState, dictionaries: dictionaries})
        },
        dictPagination: initPagination,
        setDictPagination: (pagination) => {
            return setState({...getState, dictPagination: pagination})
        }
    }
}