import {fetchAPI} from "@/api/index.ts";
import type {model} from "@/store/model/types.ts";

export const getAllModels = async()=>{
    return fetchAPI.req<model[]>('/model/getmodels', {method: "GET"})
}