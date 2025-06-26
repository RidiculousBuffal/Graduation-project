import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {createInspectionRecordSlice, type InspectionRecordSlice} from "./inspectionRecordSlice.ts";

export type InspectionState = InspectionRecordSlice

export const useInspectionStore = create<InspectionState>()(
    persist(
        immer(
            (...a) => ({
                ...createInspectionRecordSlice(...a)
            })
        ),
        {
            name: "inspectionRecords",
            partialize: (state) => {
                return {
                    inspectionRecords: state.inspectionRecords
                }
            }
        }
    )
)