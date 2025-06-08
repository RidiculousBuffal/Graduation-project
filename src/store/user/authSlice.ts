import {
    type access_tokenType,
    type permissionType,
    type refresh_tokenType,
    type roleType
} from "./types.ts";
import type {StateCreator} from "zustand/vanilla";
import type {UserState} from "./userStore.ts";
import type {MiddlewareTypes} from "../baseType.ts";


export interface AuthSlice {
    access_token: access_tokenType,
    setAccessToken: (token: access_tokenType) => void
    refresh_token: refresh_tokenType
    setRefreshToken: (token: refresh_tokenType) => void
    permissions: permissionType
    setPermissions: (permissions: permissionType) => void
    roles: roleType
    setRoles: (roles: roleType) => void

}

export const createAuthSlice: StateCreator<UserState, MiddlewareTypes, [], AuthSlice> = (setState,) => ({
    access_token: null,
    refresh_token: null,
    permissions: [],
    roles: [],
    setAccessToken: (token) => {
        setState({access_token: token})
    },
    setRefreshToken: (token) => {
        setState({refresh_token: token})
    },
    setPermissions: (permissions: permissionType) => {
        setState({permissions: permissions})
    },
    setRoles: (roles: roleType) => (
        setState({roles: roles})
    )

})