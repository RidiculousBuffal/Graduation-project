import {createCurrentSlice, type CurrentSlice} from "@/store/current/currentSlice.ts";
import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";

export type currentState = CurrentSlice

export const useCurrentStore = create<currentState>()(
    persist(
        immer(
            (...a) => ({
                ...createCurrentSlice(...a)
            })
        ),
        {
            name: 'currentStore',
            partialize: (state) => {

            }
        }
    )
)