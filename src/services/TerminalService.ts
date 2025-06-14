import type {terminalType} from "../store/terminal/types.ts";
import type {Nullable} from "../publicTypes/typeUtils.ts";
import {useTerminalStore} from "../store/terminal/terminalStore.ts";
import {createTerminal, deleteTerminal, searchTerminal, updateTerminal} from "../api/terminalapi.ts";
import {BaseService} from "./BaseService.ts";

export class TerminalService extends BaseService {
    public static async getTerminalList(searchParams: Nullable<Omit<terminalType, 'terminal_id'>>) {
        // merge with pagination
        const payload = {
            ...searchParams,
            ...useTerminalStore.getState().pagination
        }
        const searchData = await searchTerminal(payload)
        return this.processResultSync(
            searchData,
            () => {
                useTerminalStore.getState().setTerminals(
                    searchData!.data
                );
                useTerminalStore.getState().setPagination(
                    searchData!.pagination
                )
            },
            () => {
            })
    }

    public static async createTerminal(terminal: Omit<terminalType, 'terminal_id'>) {
        const res = await createTerminal(terminal)
        return await this.processResultAsync(res, async () => {
            await this.getTerminalList({terminal_name: null, description: null})
        })
    }

    public static async updateTerminal(terminal: terminalType) {
        const res = await updateTerminal(terminal)
        return this.processResultSync(res, () => {
            useTerminalStore.getState().updateTerminal(terminal)
        })
    }

    public static async deleteTerminal(terminal_id: string) {
        const res = await deleteTerminal(terminal_id)
        return await this.processResultAsync(res, async () => {
                await this.getTerminalList({terminal_name: null, description: null})
            }
        )
    }
}