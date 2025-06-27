import type {EasySlice, MiddlewareTypes} from "@/store/baseType.ts";
import type {AdminUserDTO, AdminUserDTOWithRolesAndPermissions} from "@/store/admin/types.ts";
import type {StateCreator} from "zustand/vanilla";
import type {AdminState} from "@/store/admin/adminStore.ts";
import {initPagination} from "@/publicTypes/pagination.ts";

export type AdminUsersSlice = EasySlice<'user', AdminUserDTOWithRolesAndPermissions, AdminUserDTOWithRolesAndPermissions>
export const createAdminUsersSlice: StateCreator<AdminState, MiddlewareTypes, [], AdminUsersSlice> = (setState, getState) => {
    return {
        users: [],
        usersPagination: initPagination,
        updateUser: (obj) => {
            const currentState = getState()
            const newUsers = currentState.users.map(x => {
                if (x.user_id == obj.user_id) {
                    return obj
                } else {
                    return x
                }
            })
            setState(
                {
                    ...getState(),
                    users: newUsers
                }
            )
        },
        setUsers: (obj) => {
            setState(
                {
                    ...getState,
                    users: obj
                }
            )
        },
        setUsersPagination: (obj) => {
            setState(
                {
                    ...getState(),
                    usersPagination: obj
                }
            )
        }
    }
}