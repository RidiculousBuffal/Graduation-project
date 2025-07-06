---
next:
  text: 登录/注册/刷新令牌
  link: /docs/api/auth
---

# 开始

> 本板块对各个接口进行详细说明

# BaseUrl与基本返回值格式

### BaseUrl:

```bash
http://localhost:5000/api
```

## 返回值格式:

> 如果是程序自身的问题发生异常,会返回400,500,404等状态码,如果是因为用户请求的问题,如字段不存在,操作失败等,统一返回200,用code表示失败和成功

| 字段名  | 类型     | 描述          |
|------|--------|-------------|
| code | int    | 1表示失败,0表示成功 |
| msg  | string | 描述          |
| data | object | 负载          |

## 鉴权请求头:

以`Bearer {token}`形式放到`header`里,如下,后端自动校验权限,角色

```bash
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDQzMTkwNSwianRpIjoiNmU4ZGY4MzEtYTUyMi00ZWQxLTk4ZmItMGRmNGQ3Y2EwNjNlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVmODlkY2I2LWUzMTAtNDQxNy1iMDQ3LWMxM2U3NWQ5MWVhMCIsIm5iZiI6MTc0NDQzMTkwNSwiY3NyZiI6ImE2MWNmNzhiLWIyYjItNGUzMS1iYWVkLTkxMzI3MzljMjIwNyIsImV4cCI6MTc0NDUxODMwNX0.uVq_MUZt0M9uUs2dKG4Pm8UjwoLjtYO6X6ZvWDzGZKU
```

## 权限不足时的返回

所有权限校验不通过时,返回格式如下:状态码**403**

```json
{
  "code": 1,
  "data": null,
  "msg": "权限校验失败,要求权限:['AIRCRAFT.ADD']"
}
```

## 基本请求示例:

```typescript
import {useUserStore} from "../store/user/userStore.ts";
import message from "../components/globalMessage/globalMessage.ts";
import {NET_WORK_ERROR, TOKEN_EXPIRED, TOKEN_HAS_EXPIRED, TOKEN_NOT_FOUND, UNAUTHORIZED} from "../consts/apiConsts.ts";
import {initUserInfoState} from "../store/user/initState.ts";

export interface Result<T> {
    code: number
    data: T
    msg: string
}

const BASE_URL = import.meta.env.VITE_APP_API_URL
const whiteList = ['/auth/login', '/auth/register', '/auth/loginByFaceInfo']
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
            if (result.code === 0) {
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
            if (!(options.body instanceof FormData)) {
                options.headers = {
                    ...options.headers,
                    'Content-Type': 'application/json'
                }
            }
        }
        const res = await fetch(`${this.BASE_URL}${url}`, options)
        if (!res.ok) {
            if (res.status === 401) {
                const result: { msg: string } = await res.json()
                if (result.msg === TOKEN_HAS_EXPIRED) {
                    const token = await this.refreshToken()
                    if (token) {
                        //     刷新令牌成功
                        return this.req(url, options);
                    } else {
                        //     刷新令牌失败,身份过期
                        useUserStore.getState().setUser(initUserInfoState)
                        useUserStore.getState().setRefreshToken(null)
                        useUserStore.getState().setAccessToken(null)
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
```