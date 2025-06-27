import type {EasySlice, MiddlewareTypes} from "@/store/baseType.ts";
import type {Role, RolePermission} from "@/store/admin/types.ts";
import type {StateCreator} from "zustand/vanilla";
import type {AdminState} from "@/store/admin/adminStore.ts";
import {initPagination} from "@/publicTypes/pagination.ts";

export type RoleSlice = EasySlice<'role', RolePermission, RolePermission>

export const createRoleSlice: StateCreator<AdminState, MiddlewareTypes, [], RoleSlice> = (setState, getState) => {
    return {
        roles: [],
        rolesPagination: initPagination,
        setRoles: (roles) => {
            setState({
                ...getState,
                roles: roles
            })
        },
        updateRole: (role) => {
            const currentState = getState()
            const newRole = currentState.roles.map(x => {
                if (x.role.role_id == role.role.role_id) {
                    return role
                } else {
                    return x
                }
            })
            setState(
                {
                    ...getState,
                    roles: newRole
                }
            )
        },
        setRolesPagination: (obj) => {
            setState({
                ...getState(),
                rolesPagination: obj
            })
        }
    }
}