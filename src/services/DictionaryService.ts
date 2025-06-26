import {BaseService} from "./BaseService.ts";
import {
    getChildrenByParentId,
    getDictionaryById,
    searchDictionary,
    type SearchDictionaryPayload
} from "@/api/dictionaryapi.ts";
import {useDictionaryStore} from "@/store/dictionary/DictionaryStore.ts";

export class DictionaryService extends BaseService {
    public static async getDictionaryById(id: string) {
        return await getDictionaryById(id)
    }

    public static async getDictionaryList(searchParams: SearchDictionaryPayload) {
        const payload = {
            ...searchParams,
            ...useDictionaryStore.getState().dictPagination
        }
        const searchData = await searchDictionary(payload)
        return this.processResultSync(
            searchData, () => {
                useDictionaryStore.getState().setDictionaries(searchData?.data!)
            }
        )
    }

    public static async getChildrenByParentId(parentId: string) {
        return await getChildrenByParentId(parentId)
    }
}