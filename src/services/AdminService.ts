import {BaseService} from "@/services/BaseService.ts";
import {
    getRolePermList,
    type SearchUserPayload,
    searchUser,
    getPermissionList,
    type forceUpdateUserPasswordPayload,
    type updateRolePermPayload,
    updateRolePerm,
    type updateUserRolePayload,
    updateUserRole,
    createRole,
    forceUpdateUserPassword, deleteRole
} from "@/api/adminapi.ts";
import {useAdminStore} from "@/store/admin/adminStore.ts";
import type {AdminUserDTO, Role} from "@/store/admin/types.ts";
import {forceUpdateUserInfo, updateUserInfo} from "@/api/userapi.ts";
import type {userType} from "@/store/user/types.ts";

export class AdminService extends BaseService {
    public static async getUsersList(searchParams: SearchUserPayload) {
        const payload = {
            ...searchParams,
            ...useAdminStore.getState().usersPagination
        }
        const searchData = await searchUser(payload)
        return this.processResultSync(searchData, () => {
            useAdminStore.getState().setUsers(searchData?.data!)
            useAdminStore.getState().setUsersPagination(searchData?.pagination!)
        })
    }

    public static async getRolesPermsList() {
        const data = await getRolePermList()
        return this.processResultSync(data, () => {
            useAdminStore.getState().setRoles(data!)
        })
    }

    public static async getPermissionList() {
        return await getPermissionList()
    }

    public static async updateRolePerm(payload: updateRolePermPayload) {
        const data = updateRolePerm(payload)
        return this.processResultAsync(data, async () => {
            await this.getRolesPermsList()
        })
    }

    public static async updateUserRole(payload: updateUserRolePayload) {
        const data = updateUserRole(payload)
        return this.processResultAsync(data, async () => {
            await this.getUsersList({})
        })
    }

    public static async createRole(payload: Omit<Role, 'role_id'>) {
        const res = await createRole(payload)
        return this.processResultAsync(res, async () => {
            await this.getRolesPermsList()
        })
    }

    public static async forceUpdateUserPassword(payload: forceUpdateUserPasswordPayload) {
        const res = await forceUpdateUserPassword(payload)
        return this.processResultAsync(res, async () => {
            await this.getUsersList({})
        })
    }

    public static async deleteRole(roleId: number) {
        const res = await deleteRole(roleId)
        return this.processResultAsync(res, async () => {
            await this.getRolesPermsList()
        })
    }

    public static async forceUpdateUserInfo(user: Partial<AdminUserDTO>) {
        const res = await forceUpdateUserInfo(user as Partial<userType>)
        return this.processResultAsync(res, async () => {
            await this.getUsersList({})
        })
    }
}