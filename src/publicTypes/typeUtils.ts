export type Nullable<T> = T extends object
    ? { [P in keyof T]: Nullable<T[P]> }
    : T | null | undefined;

type ShouldKeep = (value: any) => boolean;

export function clean<T>(o: T, shouldKeep: ShouldKeep = (x) => {
    return !(x == '' || x == null || x == undefined)
}): T {
    if (Array.isArray(o)) {
        // 筛选出需要保留的，然后递归清洗元素
        // 这里只处理一级嵌套，如果需要深层过滤请自行进一步调整
        return o
            .filter(shouldKeep)
            .map(item => clean(item, shouldKeep)) as unknown as T;
    } else if (o !== null && typeof o === 'object') {
        const cleanedEntries = Object.entries(o)
            .filter(([_, v]) => shouldKeep(v))
            .map(([k, v]) => [k, clean(v, shouldKeep)]);
        return Object.fromEntries(cleanedEntries) as T;
    } else {
        return o;
    }
}