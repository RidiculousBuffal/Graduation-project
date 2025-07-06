# 强制修改用户信息

## 接口地址

`/auth/forceUpdateInfo`

## 传入参数

• 要求鉴权：是（Permission: USER_UPDATE）

• 请求方式：POST

• 传入方式：JSON

• 要求权限：用户信息修改授权

| **参数名**    | **描述** | **是否必须** | **类型** |
|------------|--------|----------|--------|
| user_id    | 用户ID   | 是        | str    |
| email      | 邮箱     | 否        | str    |
| phone      | 手机     | 否        | str    |
| name       | 姓名     | 否        | str    |
| gender     | 性别     | 否        | str    |
| work_years | 工龄     | 否        | int    |
| department | 部门     | 否        | str    |
| faceInfo   | 人脸识别信息 | 否        | str    |

## 返回值——成功

```json
{
  "code": 0,
  "msg": "用户信息修改成功",
  "data": {
    "user_id": "1",
    "email": "..."
  }
}
```

:::info
返回 user 信息字典，具体字段:
```typescript
export type Role = {
    role_id: number,
    role_name: string,
    description: string,
}
export type Permission = {
    permission_id: number,
    permission_name: string,
    description: string,
}
export type RolePermission = {
    role: Role,
    permissions: Permission[]
}

export interface AdminUserDTO {
    user_id: string;
    username: string;
    email?: string;
    phone?: string;
    faceInfo?: string;
    status?: boolean;
    last_login?: Date ;
    created_at?: Date ;
    updated_at?: Date ;
    name?: string;
    gender?: string;
    department?: string;
    work_years?: number;
    contact_info?: string;
}

export interface AdminUserDTOWithRolesAndPermissions extends AdminUserDTO {
    roles: Role[],
    permissions: Permission[]
}
```
:::
## 请求示例

```JavaScript
fetch("/api/auth/forceUpdateInfo", {
    method: "POST",
    headers: {
        "Authorization": "Bearer your_jwt_token",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "user_id": "1",
        "email": "test@demo.com",
        "name": "张三"
    })
});
```

---

# 修改密码

## 接口地址

`/auth/updatePassword`

## 传入参数

• 要求鉴权：是（JWT）

• 请求方式：POST

• 传入方式：JSON

• 要求权限：无，仅登录

| **参数名**     | **描述** | **是否必须** | **类型** |
|-------------|--------|----------|--------|
| password    | 原密码    | 是        | str    |
| newPassword | 新密码    | 是        | str    |

## 返回值——成功

```json
{
  "code": 0,
  "data": true,
  "msg": "密码更新成功"
}
```

## 返回值——原密码错误

```json
{
  "code": 1,
  "data": null,
  "msg": "原密码错误"
}
```

## 请求示例

```JavaScript
fetch("/api/auth/updatePassword", {
    method: "POST",
    headers: {
        "Authorization": "Bearer your_jwt_token",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "password": "oldpass",
        "newPassword": "newpass456"
    })
});
```

---

# 管理员强制重置指定用户密码

## 接口地址

`/auth/forceUpdateUserPassword`

## 传入参数

• 要求鉴权：是（Permission: USER_READ_ALL）

• 请求方式：POST

• 传入方式：JSON

• 要求权限：用户管理权限

| **参数名**  | **描述** | **是否必须** | **类型** |
|----------|--------|----------|--------|
| password | 新密码    | 是        | str    |
| userId   | 用户ID   | 是        | str    |

## 返回值——成功

```json
{
  "code": 0,
  "data": true,
  "msg": "密码更新成功"
}
```

## 请求示例

```JavaScript
fetch("/api/auth/forceUpdateUserPassword", {
    method: "POST",
    headers: {
        "Authorization": "Bearer your_jwt_token",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "userId": "123",
        "password": "newpass123"
    })
});
```

---

# 获取全部用户信息分页

## 接口地址

`/auth/getAllUserInfo`

## 传入参数

• 要求鉴权：是（Permission: USER_READ_ALL）

• 请求方式：GET

• 传入方式：Query参数

• 要求权限：用户列表读取

| **参数名**  | **描述** | **是否必须** | **类型** |
|----------|--------|----------|--------|
| username | 用户账号   | 否        | str    |
| name     | 姓名     | 否        | str    |
| email    | 邮箱     | 否        | str    |
| pageNum  | 页码     | 否        | int    |
| pageSize | 单页数量   | 否        | int    |

## 返回值——成功

```json
{
  "code": 0,
  "msg": "用户信息获取成功",
  "data": {
    "data": [
      {
        "user_id": "1",
        "username": "...",
        "roles": [],
        "permissions": []
      }
    ],
    "pagination": {
      "pageNum": 1,
      "pageSize": 10,
      "total": 100
    }
  }
}
```

## 请求示例

```JavaScript
fetch("/api/auth/getAllUserInfo?pageNum=1&pageSize=20&username=xiaoming", {
    headers: {
        "Authorization": "Bearer your_jwt_token"
    }
});
```

---

# 获取全部权限列表

## 接口地址

`/auth/getPermissionList`

## 传入参数

• 要求鉴权：是（Permission: PERMISSIONS_MANAGEMENT）

• 请求方式：GET

• 传入方式：无

• 要求权限：权限管理

| **参数名** | **描述** | **是否必须** | **类型** |
|---------|--------|----------|--------|
| 无       | -      | -        | -      |

## 返回值——成功

```json
{
  "code": 0,
  "msg": "用户信息获取成功",
  "data": [
    {
      "permission_id": 1,
      "permission_name": "xxxx",
      "description": "..."
    }
  ]
}
```

## 请求示例

```JavaScript
fetch("/api/auth/getPermissionList", {
    headers: {"Authorization": "Bearer your_jwt_token"}
});
```

---

# 获取所有角色及对应权限

## 接口地址

`/auth/getRolePermList`

## 传入参数

• 要求鉴权：是（Permission: PERMISSIONS_MANAGEMENT）

• 请求方式：GET

• 传入方式：无

• 要求权限：权限管理

| **参数名** | **描述** | **是否必须** | **类型** |
|---------|--------|----------|--------|
| 无       | -      | -        | -      |

## 返回值——成功

```json
{
  "code": 0,
  "msg": "全部角色及权限获取成功",
  "data": [
    {
      "role": {
        "role_id": 1,
        "role_name": "管理员",
        "description": ""
      },
      "permissions": [
        {
          "permission_id": 1,
          "permission_name": "...",
          "description": ""
        }
      ]
    }
  ]
}
```

## 请求示例

```JavaScript
fetch("/api/auth/getRolePermList", {
    headers: {"Authorization": "Bearer your_jwt_token"}
});
```

---

# 修改用户状态

## 接口地址

`/auth/updateUserStatus`

## 传入参数

• 要求鉴权：是（Permission: USER_READ_ALL）

• 请求方式：POST

• 传入方式：JSON

• 要求权限：用户管理

| **参数名** | **描述** | **是否必须** | **类型** |
|---------|--------|----------|--------|
| userId  | 用户ID   | 是        | str    |
| status  | 用户状态   | 是        | bool   |

## 返回值——成功

```json
{
  "code": 0,
  "msg": "用户状态更新成功",
  "data": true
}
```

## 请求示例

```JavaScript
fetch("/api/auth/updateUserStatus", {
    method: "POST",
    headers: {
        "Authorization": "Bearer your_jwt_token",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "userId": "2",
        "status": true
    })
});
```

---

# 修改角色权限

## 接口地址

`/auth/updateRolePerm`

## 传入参数

• 要求鉴权：是（Permission: PERMISSIONS_MANAGEMENT）

• 请求方式：POST

• 传入方式：JSON

• 要求权限：权限管理

| **参数名** | **描述** | **是否必须** | **类型** |
|---------|--------|----------|--------|
| roleId  | 角色ID   | 是        | int    |
| permIds | 权限ID数组 | 是        | int数组  |

## 返回值——成功

```json
{
  "code": 0,
  "msg": "角色权限更新成功",
  "data": true
}
```

## 请求示例

```JavaScript
fetch("/api/auth/updateRolePerm", {
    method: "POST",
    headers: {
        "Authorization": "Bearer your_jwt_token",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "roleId": 1,
        "permIds": [1, 2, 3]
    })
});
```

---

# 修改用户角色

## 接口地址

`/auth/updateUserRole`

## 传入参数

• 要求鉴权：是（Permission: USER_READ_ALL）

• 请求方式：POST

• 传入方式：JSON

• 要求权限：用户管理

| **参数名** | **描述** | **是否必须** | **类型** |
|---------|--------|----------|--------|
| userId  | 用户ID   | 是        | str    |
| roleIds | 角色ID数组 | 是        | int数组  |

## 返回值——成功

```json
{
  "code": 0,
  "msg": "用户角色更新成功",
  "data": true
}
```

## 请求示例

```javascript
fetch("/api/auth/updateUserRole", {
    method: "POST",
    headers: {
        "Authorization": "Bearer your_jwt_token",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "userId": "100",
        "roleIds": [2, 3]
    })
});
```

---

# 新建角色

## 接口地址

`/auth/createRole`

## 传入参数

• 要求鉴权：是（Permission: PERMISSIONS_MANAGEMENT）

• 请求方式：POST

• 传入方式：JSON

• 要求权限：权限管理

| **参数名**     | **描述** | **是否必须** | **类型** |
|-------------|--------|----------|--------|
| role_name   | 角色名称   | 是        | str    |
| description | 角色描述   | 否        | str    |

## 返回值——成功

```json
{
  "code": 0,
  "msg": "角色创建成功",
  "data": true
}
```

## 请求示例

```JavaScript
fetch("/api/auth/createRole", {
    method: "POST",
    headers: {
        "Authorization": "Bearer your_jwt_token",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "role_name": "质检员",
        "description": "主要负责检查工作"
    })
});
```

---

# 删除角色

## 接口地址

`/auth/deleteRole/<int:roleId>`

## 传入参数

• 要求鉴权：视系统策略

• 请求方式：DELETE

• 传入方式：路径参数

• 要求权限：权限管理

| **参数名** | **描述** | **是否必须** | **类型** |
|---------|--------|----------|--------|
| roleId  | 角色ID   | 是        | int    |

## 返回值——成功

```json
{
  "code": 0,
  "msg": "角色删除成功",
  "data": true
}
```

## 请求示例

```JavaScript
fetch("/api/auth/deleteRole/3", {
    method: "DELETE",
    headers: {
        "Authorization": "Bearer your_jwt_token"
    }
});
```