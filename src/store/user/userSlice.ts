import type {StateCreator} from "zustand/vanilla";
import type {UserState} from "./userStore.ts";
import type {MiddlewareTypes} from "../baseType.ts";
import {initUserInfoState} from "./initState.ts";
import type {userType} from "./types.ts";

export interface UserSlice {
    user: userType,
    setUser: (user: userType) => void
}


export const createUserSlice: StateCreator<UserState, MiddlewareTypes, [], UserSlice> = (set, get) => ({
    user: initUserInfoState,
    setUser: (userdata: userType) => {
        set({user: userdata})
    }
})