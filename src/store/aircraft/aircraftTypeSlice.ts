import type {aircraftTypeType} from "./types.ts";
import {initPagination, type Pagination} from "../../publicTypes/pagination.ts";
import type {StateCreator} from "zustand/vanilla";
import type {AircraftState} from "./aircraftStore.ts";
import type {MiddlewareTypes} from "../baseType.ts";

export interface AircraftTypeSlice {
    aircraftTypes: aircraftTypeType[],
    setAircraftTypes: (aircraftType: aircraftTypeType[]) => void
    pagination: Pagination
    setPagination: (pagination: Pagination) => void
    updateAircraftType: (aircraftType: aircraftTypeType) => void
}

export const createAircraftTypeSlice: StateCreator<AircraftState, MiddlewareTypes, [], AircraftTypeSlice> = (setState, getState, store) => {
    return {
        aircraftTypes: [],
        pagination: initPagination,
        setPagination: (pagination: Pagination) => {
            setState({...getState(), pagination: pagination})
        },
        setAircraftTypes: (aircraftTypes: aircraftTypeType[]) => {
            setState({...getState(), aircraftTypes: aircraftTypes})
        },
        updateAircraftType: (aircraftType: aircraftTypeType) => {
            const currentState = getState();
            const updatedAircraftTypes = currentState.aircraftTypes.map((existingAircraftType) => {
                if (existingAircraftType.typeid == aircraftType.typeid) {
                    return aircraftType
                } else {
                    return existingAircraftType;
                }
            })
            setState({...currentState, aircraftTypes: updatedAircraftTypes});
        }

    }
}