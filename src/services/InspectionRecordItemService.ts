import {BaseService} from "@/services/BaseService.ts";
import {useInspectionItemStore} from "@/store/inspectionItem/InspectionItemStore.ts";
import {
    createInspectionItem,
    type createInspectionItemType, deleteInspectionItem,
    searchInspectionItem,
    updateInspectionItem,
    type updateInspectionItemType
} from "@/api/inspectionItemapi.ts";
import {useCurrentStore} from "@/store/current/currentStore.ts";

export class InspectionRecordItemService extends BaseService {
    public static async getInspectionRecordItemList() {
        const params = {inspection_id: useCurrentStore.getState().currentInspectionRecord?.inspection_id!}
        const payload = {
            ...params,
            ...useInspectionItemStore.getState().inspectionItemsPagination
        }
        const searchData = await searchInspectionItem(payload)
        return this.processResultSync(searchData, () => {
            useInspectionItemStore.getState().setInspectionItems(searchData?.data!);
            useInspectionItemStore.getState().setInspectionItemsPagination(searchData?.pagination!);
        })
    }

    public static async createInspectionRecordItem(inspectionItem: createInspectionItemType) {
        const res = await createInspectionItem(inspectionItem)
        return this.processResultAsync(res, async () => {
            await this.getInspectionRecordItemList()
        })
    }

    public static async updateInspectionRecordItem(itemId: string, inspectionItem: updateInspectionItemType) {
        const res = await updateInspectionItem(itemId, inspectionItem)
        return this.processResultSync(res, () => {
            useInspectionItemStore.getState().updateInspectionItem(res!)
        })
    }
    public static async deleteInspectionRecordItem(itemId: string) {
        const res = await deleteInspectionItem(itemId)
        return await this.processResultAsync(res, async () => {
            await this.getInspectionRecordItemList()
        })
    }


}