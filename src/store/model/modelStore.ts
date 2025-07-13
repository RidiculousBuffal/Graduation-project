import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {createModelSlice, type ModelSlice} from "@/store/model/modelSlice.ts";

export type ModelState = ModelSlice
export const useModelStore = create<ModelState>()(
    persist(
        immer(
            (...a) => ({
                ...createModelSlice(...a)
            })
        ),
        {
            name: 'modelStore',
            partialize: (state) => {
                return {
                    models: state.models,
                }
            }
        }
    )
)