import {BaseService} from "@/services/BaseService.ts";
import {getBlockChainStatus, searchAuditLog} from "@/api/auditAPI.ts";
import {useLogStore} from "@/store/log/logStore.ts";

export class AuditService extends BaseService {
    public static async getAuditStatus() {
        return await getBlockChainStatus()
    }
    public static async getAuditLog() {
        const payload = {
            ...useLogStore.getState().logsPagination
        }
        const data = await searchAuditLog(payload)
        return this.processResultSync(
            data,
            () => {
                useLogStore.getState().setLogs(data!.data!)
                useLogStore.getState().setLogsPagination(data!.pagination!)
            },
            () => {
            }
        )
    }
}