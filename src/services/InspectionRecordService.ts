import {BaseService} from "@/services/BaseService.ts";
import {
    searchInspectionRecords,
    type SearchInspectionRecordPayload,
    type createInspectionRecordPayload, createInspectionRecord, getInspectionRecordById, updateInspectionRecord,
    deleteInspectionRecord, type updateInspectionRecordPayload
} from "@/api/inspectionRecordapi.ts";
import {useInspectionStore} from "@/store/inspection/inspectionStore.ts";

export class InspectionRecordService extends BaseService {
    public static async getInspectionRecordList(params: SearchInspectionRecordPayload) {
        const payload = {
            ...params,
            ...useInspectionStore.getState().inspectionRecordsPagination
        }
        const searchData = await searchInspectionRecords(payload)
        return this.processResultSync(searchData, () => {
            useInspectionStore.getState().setInspectionRecords(searchData?.data!);
            useInspectionStore.getState().setInspectionRecordsPagination(searchData?.pagination!);
        })
    }

    public static async createInspectionRecord(inspectionRecord: createInspectionRecordPayload) {
        const res = await createInspectionRecord(inspectionRecord)
        return this.processResultAsync(res, async () => {
            await this.getInspectionRecordList({})
        })
    }

    public static async getInspectionRecordById(inspectionRecordId: string) {
        return getInspectionRecordById(inspectionRecordId)
    }

    public static async updateInspectionRecord(inspectionRecord: updateInspectionRecordPayload) {
        const res = await updateInspectionRecord(inspectionRecord)
        return this.processResultSync(res, () => {
            useInspectionStore.getState().updateInspectionRecord(res!)
        })
    }

    public static async deleteInspectionRecord(inspectionRecordId: string) {
        const res = await deleteInspectionRecord(inspectionRecordId)
        return await this.processResultAsync(res, async () => {
            await this.getInspectionRecordList({})
        })
    }
}