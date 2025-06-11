import {useUserStore} from "../store/user/userStore.ts";
import message from "../components/globalMessage/globalMessage.ts";
import {NET_WORK_ERROR, TOKEN_EXPIRED, TOKEN_NOT_FOUND, UNAUTHORIZED} from "../consts/apiConsts.ts";
import {initUserInfoState} from "../store/user/initState.ts";

export interface Result<T> {
    code: number
    data: T
    msg: string
}

const BASE_URL = import.meta.env.VITE_APP_API_URL
const whiteList = ['/auth/login', '/auth/register','/auth/loginByFaceInfo']
const refreshEndPoint = '/auth/refresh'

class MyFetch {
    private readonly BASE_URL: string
    private readonly RefreshEndPoint: string
    private readonly whiteList: string[]

    constructor(BASE_URL: string, RefreshEndPoint: string, whiteList: string[]) {
        this.BASE_URL = BASE_URL
        this.RefreshEndPoint = RefreshEndPoint
        this.whiteList = whiteList
    }

    private refreshToken = async () => {
        const refreshToken = useUserStore.getState().refresh_token
        if (!refreshToken) {
            return null
        }
        try {
            const res = await fetch(`${this.BASE_URL}${this.RefreshEndPoint}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${refreshToken}`
                }
            })
            if (!res.ok) {
                return null
            }
            const result: Result<{ access_token: string }> = await res.json()
            if (result.code === 200) {
                useUserStore.getState().setAccessToken(result.data.access_token)
                return result.data.access_token
            }
            return null
        } catch (e) {
            return null
        }
    }
    public req = async <T>(url: string, options: RequestInit = {}): Promise<T | null> => {

        if (!this.whiteList.includes(url)) {
            //   非白名单里面的,要加上请求头
            const accessToken = useUserStore.getState().access_token
            if (!accessToken) {
                message.error(TOKEN_NOT_FOUND)
                return null
            }
            options.headers = {
                ...options.headers,
                Authorization: `Bearer ${accessToken}`
            }
        }

        if (!options.headers || !('Content-Type' in options.headers)) {
            options.headers = {
                ...options.headers,
                'Content-Type': 'application/json'
            }
        }

        const res = await fetch(`${this.BASE_URL}${url}`, options)
        if (!res.ok) {
            if (res.status === 401) {
                const result: { msg: string } = await res.json()
                if (result.msg === TOKEN_EXPIRED) {
                    const token = await this.refreshToken()
                    if (token) {
                        //     刷新令牌成功
                        return this.req(url, options);
                    } else {
                        //     刷新令牌失败,身份过期
                        useUserStore.getState().setUser(initUserInfoState)
                        useUserStore.getState().setRefreshToken(null)
                        useUserStore.getState().setRefreshToken(null)
                        useUserStore.getState().setPermissions([])
                        useUserStore.getState().setRoles([])
                        message.error(TOKEN_EXPIRED)
                        return null
                    }
                } else {
                    message.error(UNAUTHORIZED)
                    return null
                }
            } else {
                message.error(NET_WORK_ERROR)
                return null
            }
        }
        const result: Result<T> = await res.json()
        if (result.code == 0) {
            return result.data
        } else {
            message.error(result.msg)
            return null;
        }
    }
}

export const fetchAPI = new MyFetch(BASE_URL, refreshEndPoint, whiteList)