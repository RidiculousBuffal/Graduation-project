import type {AircraftArrayType} from "./types.ts";
import type {aircraftType_} from "./types.ts";
import {initPagination, type Pagination} from "../../publicTypes/pagination.ts";
import type {StateCreator} from "zustand/vanilla";
import type {AircraftState} from "./aircraftStore.ts";
import type {MiddlewareTypes} from "../baseType.ts";

export interface AircraftSlice {
    aircrafts: AircraftArrayType,
    setAircrafts: (aircrafts: AircraftArrayType) => void
    updateAircraft: (aircraft: aircraftType_) => void
    aircraftPagination: Pagination
    setAircraftPagination: (pagination: Pagination) => void
}

export const createAircraftSlice: StateCreator<AircraftState, MiddlewareTypes, [], AircraftSlice> = (setState, getState, store) => {
    return {
        aircraftPagination: initPagination,
        aircrafts: [],
        updateAircraft: (aircraft: aircraftType_) => {
            const currentState = getState()
            const updateAircrafts = currentState.aircrafts.map((existingAircraft) => {
                if (existingAircraft.aircraft_id == aircraft.aircraft_id) {
                    return {...existingAircraft, ...aircraft}
                } else {
                    return existingAircraft
                }
            })
            setState({...currentState, aircrafts: updateAircrafts})
        },
        setAircrafts: (aircrafts: AircraftArrayType) => {
            setState({...getState(), aircrafts: aircrafts})
        },
        setAircraftPagination: (pagination: Pagination) => {
            setState({...getState(), aircraftPagination: pagination})
        }
    }
}