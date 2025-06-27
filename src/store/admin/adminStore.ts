import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {createRoleSlice, type RoleSlice} from "@/store/admin/roleSlice.ts";
import {type AdminUsersSlice, createAdminUsersSlice} from "@/store/admin/usersSlice.ts";

export type AdminState = RoleSlice & AdminUsersSlice
export const useAdminStore = create<AdminState>()(
    persist(
        immer(
            (...a) => {
                return {
                    ...createAdminUsersSlice(...a),
                    ...createRoleSlice(...a)
                }
            }
        ), {
            name: "adminUserStore",
            partialize: (state) => {
                return {
                    roles: state.roles,
                    users: state.users,
                }
            }
        }
    )
)