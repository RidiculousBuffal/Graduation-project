import {BaseService} from "./BaseService.ts";
import type {Nullable} from "../publicTypes/typeUtils.ts";
import type {aircraftTypeType} from "../store/aircraft/types.ts";
import {useAircraftStore} from "../store/aircraft/aircraftStore.ts";
import {createAircraftType, deleteAircraftType, searchAircraftType, updateAircraftType} from "../api/aircraftapi.ts";

export class AircraftTypeService extends BaseService {
    public static async getAircraftTypeList(searchParams: Nullable<Omit<aircraftTypeType, 'typeid'>>) {
        // merge with pagination
        const payload = {
            ...searchParams,
            ...useAircraftStore.getState().pagination
        }
        const searchData = await searchAircraftType(payload)
        return this.processResultSync(
            searchData,
            () => {
                useAircraftStore.getState().setAircraftTypes(
                    searchData!.data
                );
                useAircraftStore.getState().setPagination(
                    searchData!.pagination
                )
            },
            () => {
            })
    }

    public static async createAircraftType(aircraftType: Partial<aircraftTypeType>) {
        const res = await createAircraftType(aircraftType)
        return await this.processResultAsync(res, async () => {
            await this.getAircraftTypeList({type_name: null, description: null})
        })
    }

    public static async updateTerminal(aircraftType: aircraftTypeType) {
        const res = await updateAircraftType(aircraftType)
        return this.processResultSync(res, () => {
            useAircraftStore.getState().updateAircraftType(aircraftType)
        })
    }

    public static async deleteAircraftType(aircraftTypeId: string) {
        const res = await deleteAircraftType(aircraftTypeId)
        return await this.processResultAsync(res, async () => {
                await this.getAircraftTypeList({type_name: null, description: null})
            }
        )
    }
}