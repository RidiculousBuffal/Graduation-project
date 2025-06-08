import {create} from "zustand";
import {persist} from "zustand/middleware";
import {immer} from "zustand/middleware/immer";
import {createUserSlice, type UserSlice} from "./userSlice.ts";
import {type AuthSlice, createAuthSlice} from "./authSlice.ts";

export type UserState = UserSlice & AuthSlice
export const useUserStore = create<UserState>()(
    persist(
        immer(
            (...a) => ({
                ...createAuthSlice(...a),
                ...createUserSlice(...a)
            })
        ),
        {
            name: 'userStore',
            partialize: (state) => ({
                user: state.user,
                permissions: state.permissions,
                roles: state.roles,
                access_token: state.access_token,
                refresh_token: state.refresh_token,
            })
        }
    )
)