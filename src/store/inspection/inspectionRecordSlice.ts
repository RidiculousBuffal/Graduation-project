import type {EasySlice, MiddlewareTypes} from "@/store/baseType.ts";
import type {InspectionRecordType, InspectionRecordListType} from "@/store/inspection/types.ts";
import type {StateCreator} from "zustand/vanilla";
import type {InspectionState} from "@/store/inspection/inspectionStore.ts";
import {initPagination} from "@/publicTypes/pagination.ts";

export type InspectionRecordSlice = EasySlice<'inspectionRecord', InspectionRecordListType, InspectionRecordType>

export const createInspectionRecordSlice: StateCreator<InspectionState, MiddlewareTypes, [], InspectionRecordSlice> = (setState, getState, store) => {
    return {
        inspectionRecords: [],
        inspectionRecordsPagination: initPagination,
        setInspectionRecords: (obj) => {
            setState(
                {
                    ...getState,
                    inspectionRecords: obj
                }
            )
        },
        setInspectionRecordsPagination: (page) => {
            setState({
                ...getState,
                inspectionRecordsPagination: page
            })
        },
        updateInspectionRecord: (inspectionRecord) => {
            const currentState = getState()
            const newList = currentState.inspectionRecords.map((x) => {
                if (x.inspection_id == inspectionRecord.inspection_id) {
                    return {
                        ...x,
                        ...inspectionRecord
                    }
                } else {
                    return x
                }
            })
            setState(
                {
                    ...currentState,
                    inspectionRecords: newList
                }
            )
        }
    }
}