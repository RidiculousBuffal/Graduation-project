export type dictionaryType = {
    dict_key: string
    dict_name: string,
    description?: string
    parent_key: string
    sort_order: number
    created_at: string
    updated_at: string
    children: dictionaryType[]
};
