import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {type AircraftTypeSlice, createAircraftTypeSlice} from "./aircraftTypeSlice.ts";
import {type AircraftSlice, createAircraftSlice} from "./aircraftSlice.ts";
import {type AircraftImageSlice, createAircraftImageSlice} from "./aircraftImageSlice.ts";

export type AircraftState = AircraftTypeSlice & AircraftSlice & AircraftImageSlice
export const useAircraftStore = create<AircraftState>()(
    persist(
        immer(
            (...a) => ({
                ...createAircraftTypeSlice(...a),
                ...createAircraftSlice(...a),
                ...createAircraftImageSlice(...a)
            })
        ),
        {
            name: 'aircraftStore',
            partialize: (state) => {
                return {
                    aircraftTypes: state.aircraftTypes,
                    aircrafts: state.aircrafts,
                    images: state.images,
                }
            }
        }
    )
)