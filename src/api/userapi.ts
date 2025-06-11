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

export type loginResp = {
    access_token: string,
    payload: {
        permissions: permissionType,
        role: roleType,
        user: userType
    },
    refresh_token: string,
}

export async function login(username: string, password: string) {
    const payload = {
        username: username,
        password: password,
    }
    return fetchAPI.req<loginResp>('/auth/login', {method: "POST", body: JSON.stringify(payload)})
}

export async function updateUserInfo(user: Partial<userType>): Promise<userType | null> {
    return fetchAPI.req('/auth/updateInfo', {method: "POST", body: JSON.stringify(user)})
}

export async function updateUserFaceInfo(faceInfo: string): Promise<string | null> {
    return fetchAPI.req('/auth/updateFaceInfo', {method: "POST", body: JSON.stringify({faceInfo: faceInfo})})
}

export async function updateUserPassword(password: string, newPassword: string): Promise<boolean | null> {
    return fetchAPI.req('/auth/updatePassword', {
        method: "POST",
        body: JSON.stringify({password: password, newPassword: newPassword})
    })
}

export async function loginByFaceInfo(faceInfo: string) {
    return fetchAPI.req<loginResp>('/auth/loginByFaceInfo', {method: "POST", body: JSON.stringify({faceInfo: faceInfo})})
}