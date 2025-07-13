import {BaseService} from "./BaseService.ts";
import type {AircraftImageType} from "../store/aircraft/types.ts";
import {useAircraftStore} from "../store/aircraft/aircraftStore.ts";
import {
    createAircraftImage,
    deleteAircraftImage, getAircraftImageById,
    searchAircraftImage,
    updateAircraftImage
} from "../api/aircraftapi.ts";

export class AircraftImageService extends BaseService {
    private static IMAGE_INIT = {
        image_name: undefined,
        aircraft_id: undefined,
        aircraft_name: undefined
    }

    public static async getAircraftImageList(searchParams: {
        image_name?: string,
        aircraft_id?: string,
        aircraft_name?: string
    }) {
        // merge with pagination
        const payload = {
            ...searchParams,
            ...useAircraftStore.getState().aircraftImagePagination
        }
        const searchData = await searchAircraftImage(payload)

        return this.processResultSync(
            searchData,
            () => {
                useAircraftStore.getState().setImages(
                    searchData!.data
                );
                useAircraftStore.getState().setAircraftImagePagination(
                    searchData!.pagination
                )
            },
            () => {
            })
    }

    public static async createAircraftImage(aircraftImage: Partial<AircraftImageType>) {
        const res = await createAircraftImage(aircraftImage)
        return await this.processResultAsync(res, async () => {
            await this.getAircraftImageList(this.IMAGE_INIT)
        })
    }

    public static async updateAircraftImage(aircraftImage: AircraftImageType) {
        const res = await updateAircraftImage(aircraftImage)
        return this.processResultSync(res, () => {
            useAircraftStore.getState().updateImage(aircraftImage)
        })
    }

    public static async deleteAircraftImage(imageId: string) {
        const res = await deleteAircraftImage(imageId)
        return await this.processResultAsync(res, async () => {
            await this.getAircraftImageList(this.IMAGE_INIT)
        })
    }

    public static async getAircraftImagesByAircraftId(aircraftId: string) {
        return await this.getAircraftImageList({
            aircraft_id: aircraftId
        })
    }

    public static async getAircraftImageById(imageId: string) {
        return await getAircraftImageById(imageId);
    }
}