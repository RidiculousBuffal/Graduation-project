import type {Pagination, PaginationResult} from "@/publicTypes/pagination.ts";
import {fetchAPI} from "@/api/index.ts";
import qs from "qs";
import {clean} from "@/publicTypes/typeUtils.ts";
import type {
    AdminUserDTOWithRolesAndPermissions,
    Permission,
    Role,
    RolePermission
} from "@/store/admin/types.ts";

export type SearchUserPayload = {
    username?: string,
    name?: string,
    email?: string,
}
export const searchUser = async (request: SearchUserPayload & Pagination) => {
    const {total_pages, total, ...rest} = request
    const payload = qs.stringify(clean(rest))
    return fetchAPI.req<PaginationResult<AdminUserDTOWithRolesAndPermissions>>(`/auth/getAllUserInfo?${payload}`, {method: "GET"})
}
export const getPermissionList = async () => {
    return fetchAPI.req<Permission[]>('/auth/getPermissionList', {method: "GET"})
}
export const getRolePermList = async () => {
    return fetchAPI.req<RolePermission[]>('/auth/getRolePermList', {method: "GET"})
}
export type updateUserStatusPayload = {
    userId: string, status: boolean
}
export const updateUserStatus = async (payload: updateUserStatusPayload) => {
    return fetchAPI.req<boolean>('/auth/updateUserStatus', {method: "POST", body: JSON.stringify(payload)})
}
export type updateRolePermPayload = {
    roleId: string, permIds: number[]
}
export const updateRolePerm = async (payload: updateRolePermPayload) => {
    return fetchAPI.req<boolean>('/auth/updateRolePerm', {method: "POST", body: JSON.stringify(payload)})
}
export type updateUserRolePayload = {
    userId: string, roleIds: number[],
}
export const updateUserRole = async (payload: updateUserRolePayload) => {
    return fetchAPI.req<boolean>('/auth/updateUserRole', {method: "POST", body: JSON.stringify(payload)})
}
export const createRole = async (role: Omit<Role, 'role_id'>) => {
    return fetchAPI.req<boolean>('/auth/createRole', {method: "POST", body: JSON.stringify(role)})
}
export type forceUpdateUserPasswordPayload = {
    userId: string, password: string,
}
export const forceUpdateUserPassword = async (payload: forceUpdateUserPasswordPayload) => {
    return fetchAPI.req<boolean>('/auth/forceUpdateUserPassword', {method: "POST", body: JSON.stringify(payload)})
}
export const deleteRole = async (roleId: number) => {
    return fetchAPI.req<boolean>(`/auth/deleteRole/${roleId}`, {method: "DELETE"})
}
