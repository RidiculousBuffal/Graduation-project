import {BaseService} from "./BaseService.ts";
import {
    autocompleteFlightId,
    createFlight,
    type createFlightPayLoad, deleteFlight,
    getFlightDetailById, searchFlight,
    type SearchFlightPayload, updateFlight
} from "../api/flightapi.ts";
import type {flightType} from "../store/flight/types.ts";
import {useFlightStore} from "../store/flight/flightStore.ts";
import type {Nullable} from "../publicTypes/typeUtils.ts";

export class FlightService extends BaseService {
    public static async getFlightList(params: Nullable<SearchFlightPayload>) {
        const payload = {
            ...params,
            ...useFlightStore.getState().flightsPagination
        }
        const searchData = await searchFlight(payload)
        return this.processResultSync(
            searchData,
            () => {
                useFlightStore.getState().setFlights(
                    searchData?.data!
                );
                useFlightStore.getState().setFlightsPagination(
                    searchData?.pagination!
                )
            }
        )
    }

    public static async createFlight(flight: createFlightPayLoad) {
        const res = await createFlight(flight)
        return this.processResultAsync(res,
            async () => {
                await this.getFlightList({})
            }
        )
    }

    public static async getFlightDetailById(flightId: string) {
        return await getFlightDetailById(flightId)
    }

    public static async updateFlight(flight: flightType) {
        const res = await updateFlight(flight)
        return this.processResultSync(res,
            () => {
                useFlightStore.getState().updateFlight(flight)
            }
        )
    }

    public static async deleteFlight(flightId: string) {
        const res = await deleteFlight(flightId)
        return await this.processResultAsync(res, async () => {
            await this.getFlightList({})
        })
    }

    public static async autocompleteFlightId(payload: string) {
        /*
        *  传入payload 可以是flight_id的一部分,也可以是飞机名称的一部分,快速找到flightid
        * */
        return await autocompleteFlightId(payload)
    }
}