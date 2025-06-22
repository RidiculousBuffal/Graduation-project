import {createFlightSlice, type FlightSlice} from "./flightSlice.ts";

import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";

export type FlightState = FlightSlice;
export const useFlightStore = create<FlightState>()(
    persist(
        immer(
            (...a) => ({
                ...createFlightSlice(...a)
            })),
        {
            name: 'flightStore', partialize: (state) => {
                return {
                    flights: state.flights,
                }
            }
        }
    )
)