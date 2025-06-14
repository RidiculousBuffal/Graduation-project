export type Pagination = {
    current_page: number,
    page_size: number,
    total: number,
    total_pages: number,
}
export type PaginationResult<T> = {
    data: T[],
    pagination: Pagination,
}

export const initPagination: Pagination = {
    current_page: 1,
    page_size: 10,
    total: 0,
    total_pages: 1
}