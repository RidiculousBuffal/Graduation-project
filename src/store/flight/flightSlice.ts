import type {flightListType, flightType} from "./types.ts";
import {initPagination, type Pagination} from "../../publicTypes/pagination.ts";
import type {StateCreator} from "zustand/vanilla";
import type {FlightState} from "./flightStore.ts";
import type {MiddlewareTypes} from "../baseType.ts";

export interface FlightSlice {
    flights: flightListType[]
    setFlights: (flights: flightListType[]) => void
    updateFlight: (flight: flightType) => void
    flightsPagination: Pagination
    setFlightsPagination: (pagination: Pagination) => void
}

export const createFlightSlice: StateCreator<FlightState, MiddlewareTypes, [], FlightSlice> = (setState, getState, store) => {
    return {
        flights: [],
        flightsPagination: initPagination,
        setFlights: (flights: flightListType[]) => {
            setState({...getState(), flights: flights})
        },
        setFlightsPagination: (pagination: Pagination) => {
            setState({...getState, flightsPagination: pagination})
        }
        ,
        updateFlight: (flight: flightType) => {
            const currentState = getState();
            const updatedFlights = currentState.flights.map(existingFlight =>
                existingFlight.flight_id === flight.flight_id
                    ? {...existingFlight,...flight}
                    : existingFlight
            );
            setState({...currentState, flights: updatedFlights});
        }
    }
}