import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {createInspectionItemSlice, type InspectionItemSlice} from "@/store/inspectionItem/InspectionItemSlice.ts";

export type InspectionItemStore = InspectionItemSlice
export const useInspectionItemStore = create<InspectionItemStore>()(
    persist(
        immer(
            (...a) => ({
                ...createInspectionItemSlice(...a)
            })
        ),
        {
            name: 'InspectionItemStore',
            partialize: (state) => {
                return {
                    inspectionItems: state.inspectionItems
                }
            }
        }
    )
)