import {BaseService} from "./BaseService.ts";
import type {Nullable} from "../publicTypes/typeUtils.ts";
import type {aircraftType_, aircraftTypeType} from "../store/aircraft/types.ts";
import {useAircraftStore} from "../store/aircraft/aircraftStore.ts";
import {createAircraft, deleteAircraft, searchAircraft, updateAircraft} from "../api/aircraftapi.ts";

export class AircraftListService extends BaseService {
    public static async getAircraftList(searchParams: Nullable<Omit<aircraftType_ & aircraftTypeType, 'aircraft_id' | 'typeid'>>) {
        // merge with pagination
        const payload = {
            ...searchParams,
            ...useAircraftStore.getState().aircraftPagination
        }
        const searchData = await searchAircraft(payload)
        return this.processResultSync(
            searchData,
            () => {
                useAircraftStore.getState().setAircrafts(
                    searchData!.data
                );
                useAircraftStore.getState().setAircraftPagination(
                    searchData!.pagination
                )
            },
            () => {
            })
    }

    public static async createAircraft(aircraft: Partial<aircraftType_>) {
        const res = await createAircraft(aircraft)
        return await this.processResultAsync(res, async () => {
            await this.getAircraftList({aircraft_name: null, age: null, type_name: null, description: null})
        })
    }

    public static async updateAircraft(aircraft: aircraftType_) {
        const res = await updateAircraft(aircraft)
        return this.processResultSync(res, () => {
            useAircraftStore.getState().updateAircraft(aircraft)
        })
    }

    public static async deleteAircraft(aircraft: aircraftType_) {
        const res = await deleteAircraft(aircraft)
        return await this.processResultAsync(res, async () => {
            await this.getAircraftList({aircraft_name: null, age: null, type_name: null, description: null})
        })
    }
}