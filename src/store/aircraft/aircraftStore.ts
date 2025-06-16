import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {type AircraftTypeSlice, createAircraftTypeSlice} from "./aircraftTypeSlice.ts";
import {type AircraftSlice, createAircraftSlice} from "./aircraftSlice.ts";

export type AircraftState = AircraftTypeSlice & AircraftSlice
export const useAircraftStore = create<AircraftState>()(
    persist(
        immer(
            (...a) => ({
                ...createAircraftTypeSlice(...a),
                ...createAircraftSlice(...a)
            })
        ),
        {
            name: 'aircraftStore',
            partialize: (state) => {
                return {
                    aircraftTypes: state.aircraftTypes,
                    aircrafts: state.aircrafts,
                }
            }
        }
    )
)