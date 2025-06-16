import type {AircraftImageType, aircraftType_} from "./types.ts";
import {initPagination, type Pagination} from "../../publicTypes/pagination.ts";
import type {StateCreator} from "zustand/vanilla";
import type {AircraftState} from "./aircraftStore.ts";
import type {MiddlewareTypes} from "../baseType.ts";

export interface AircraftImageSlice {
    images: Array<AircraftImageType & Partial<aircraftType_>>
    setImages: (images: Array<AircraftImageType & Partial<aircraftType_>>) => void
    updateImage: (image: AircraftImageType) => void
    aircraftImagePagination: Pagination
    setAircraftImagePagination: (pagination: Pagination) => void
}

export const createAircraftImageSlice: StateCreator<AircraftState, MiddlewareTypes, [], AircraftImageSlice> = (setState, getState, store) => {
    return {
        images: [],
        aircraftImagePagination: initPagination,
        setImages: (images: Array<AircraftImageType & Partial<aircraftType_>>) => {
            setState({...getState(), images: images})
        }
        ,
        setAircraftImagePagination: (pagination: Pagination) => {
            setState({...getState(), aircraftImagePagination: pagination})
        }
        ,
        updateImage: (image: AircraftImageType) => {
            const currentState = getState();
            const updatedImages = currentState.images.map((existingImage) => {
                return existingImage.image_id == image.image_id ? {
                    ...existingImage,
                    ...image
                } : existingImage
            })
            return setState({...currentState, images: updatedImages});
        },

    }
}