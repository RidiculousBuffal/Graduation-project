import type {EasySlice, MiddlewareTypes} from "@/store/baseType.ts";
import type {InspectionItem} from "@/store/inspectionItem/types.ts";
import type {StateCreator} from "zustand/vanilla";
import type {InspectionItemStore} from "@/store/inspectionItem/InspectionItemStore.ts";
import {initPagination} from "@/publicTypes/pagination.ts";

export type InspectionItemSlice = EasySlice<'inspectionItem', InspectionItem, InspectionItem>
export const createInspectionItemSlice: StateCreator<InspectionItemStore, MiddlewareTypes, [], InspectionItemSlice> = (setState, getState, store) => {
    return {
        inspectionItems: [],
        inspectionItemsPagination: initPagination,
        setInspectionItems: (obj) => {
            setState({...getState(), inspectionItems: obj})
        },
        setInspectionItemsPagination: (obj) => {
            setState({...getState(), inspectionItemsPagination: obj})
        },
        updateInspectionItem: (obj) => {
            const currentState = getState();
            const newState = currentState.inspectionItems.map(x => {
                if (x.item_id === obj.item_id) {
                    return obj
                } else {
                    return x
                }
            })
            setState({...getState(), inspectionItems: newState})
        }
    }
}