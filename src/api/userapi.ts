import {fetchAPI} from "./index.ts";
import type {permissionType, roleType, userType} from "../store/user/types.ts";


export async function register(username: string, password: string, email: string): Promise<null> {
    const payload = {
        username: username,
        password: password,
        email: email,
    }
    return fetchAPI.req('/auth/register', {method: "POST", body: JSON.stringify(payload)})
}

export async function login(username: string, password: string) {
    const payload = {
        username: username,
        password: password,
    }
    return fetchAPI.req<{
        access_token: string,
        payload: {
            permissions: permissionType,
            role: roleType,
            user: userType
        },
        refresh_token: string,
    }>('/auth/login', {method: "POST", body: JSON.stringify(payload)})
}