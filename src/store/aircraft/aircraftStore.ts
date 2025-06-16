import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {type AircraftTypeSlice, createAircraftTypeSlice} from "./aircraftTypeSlice.ts";

export type AircraftState = AircraftTypeSlice
export const useAircraftStore = create<AircraftState>()(
    persist(
        immer(
            (...a) => ({
                ...createAircraftTypeSlice(...a)
            })
        ),
        {
            name: 'aircraftStore',
            partialize: (state) => {
                return {
                    aircraftTypes: state.aircraftTypes,
                }
            }
        }
    )
)