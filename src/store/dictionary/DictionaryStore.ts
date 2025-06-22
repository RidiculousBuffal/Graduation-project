import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {createDictionarySlice, type DictionarySlice} from "./DictionarySlice.ts";

export type DictionaryState = DictionarySlice

export const useDictionaryStore = create<DictionaryState>()(
    persist(
        immer(
            (...a) => ({
                ...createDictionarySlice(...a)
            })
        ),
        {
            name: 'dictionaryStore',
            partialize: (state) => {
                return {
                    dictionaries: state.dictionaries
                }
            }
        }
    )
)