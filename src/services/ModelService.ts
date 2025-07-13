import {getAllModels} from "@/api/modelapi.ts";
import {useModelStore} from "@/store/model/modelStore.ts";

export class ModelService {
    public static async getAllModels() {
        const data = await getAllModels()
        useModelStore.getState().setModels(data!)
    }
}