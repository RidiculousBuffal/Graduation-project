# **创建检查记录**

## **接口地址**

```bash
POST /inspection/create
```

## **鉴权/权限**

- 要求鉴权：是（JWT）
- 要求权限：INSPECTION_ADD

## **请求方式**

POST（application/json）

**参数**

| **参数名**            | **描述** | **是否必须** | **类型**          |
|--------------------|--------|----------|-----------------|
| inspection_name    | 检查名称   | 否        | string          |
| task_id            | 任务ID   | 是        | string          |
| executor_id        | 执行人    | 否        | string          |
| reference_image_id | 参考图片ID | 否        | string          |
| progress           | 检查进度   | 否        | int             |
| start_time         | 开始时间   | 否        | string(ISO8601) |
| end_time           | 结束时间   | 否        | string(ISO8601) |
| inspection_status  | 检查状态   | 否        | string          |

## **成功返回**

```json
{
  "code": 0,
  "data": {
    "inspection_id": "xxx",
    "inspection_name": "xxx",
    "task_id": "xxx",
    "progress": 0,
    "...": "更多字段"
  },
  "msg": "检查记录创建成功"
}
```

# **获取检查记录详情**

## **接口地址**

```bash
GET /inspection/getInspectionById/<inspection_id>
```

## **鉴权/权限**

- 要求鉴权：是（JWT）
- 要求权限：INSPECTION_READ

## **请求参数**

inspection_id（URL路径）

## **返回示例**

```json
{
  "code": 0,
  "data": {
    "inspection_id": "xxx",
    "inspection_name": "",
    "task_id": "xxx",
    "executor_id": "xxx",
    "executor_name": "张三",
    "reference_image_id": "img-xxx",
    "reference_image_name": "图片名字",
    "progress": 30,
    "start_time": "2024-06-20T12:35:00",
    "end_time": null,
    "inspection_status": "not_started",
    "status_name": "未开始",
    "flight_id": "flight-xxx",
    "aircraft_id": "ac-xxx",
    "aircraft_name": "波音787",
    "created_at": "2024-06-20T11:01:00",
    "updated_at": "2024-06-20T11:10:00"
  },
  "msg": "检查记录获取成功"
}
```

# **更新检查记录**

## **接口地址**

```bash
PUT /inspection/updateInspection/<inspection_id>
```

## **鉴权/权限**

- 要求鉴权：是（JWT）
- 要求权限：INSPECTION_UPDATE

## **请求体（JSON）参数**

字段同上，全部可选。

# **删除检查记录**

## **接口地址**

```bash
DELETE /api/inspection/deleteInspection/<inspection_id>
```

## **鉴权/权限**

- 要求鉴权：是（JWT）
- 要求权限：INSPECTION_DELETE

## **成功返回**

```json
{
  "code": 0,
  "msg": "检查记录删除成功"
}
```

# **分页&条件查询检查记录**

## **接口地址**

```bash
GET /inspection/search
```

## **鉴权/权限**

- 要求鉴权：是（JWT）
- 要求权限：INSPECTION_READ

## **查询参数（全部可选，分页参数必须）**

| **参数名**            | **描述** | **类型**          |
|--------------------|--------|-----------------|
| task_id            | 任务ID   | string          |
| executor_id        | 执行人ID  | string          |
| inspection_status  | 检查状态   | string          |
| reference_image_id | 参考图片ID | string          |
| flight_id          | 航班ID   | string          |
| aircraft_id        | 飞机ID   | string          |
| executor_name      | 执行人姓名  | string          |
| start_time_from    | 开始时间起  | string(ISO8601) |
| start_time_to      | 开始时间止  | string(ISO8601) |
| end_time_from      | 结束时间起  | string(ISO8601) |
| end_time_to        | 结束时间止  | string(ISO8601) |
| current_page（必须）   | 页码     | int             |
| page_size（必须）      | 每页个数   | int             |

## **返回示例**

```json
{
  "code": 0,
  "data": {
    "data": [
      {
        "inspection_id": "xxx",
        "inspection_name": "xx",
        "executor_name": "...",
        "...": "..."
      }
    ],
    "pagination": {
      "current_page": 1,
      "page_size": 10,
      "total": 53,
      "total_pages": 6
    }
  },
  "msg": "检查记录获取成功"
}
```

# 更新用户人脸信息

## 接口地址

```bash
/auth/updateFaceInfo
```

## 传入参数

- 要求鉴权：是（JWT）
- 请求方式：POST
- 传入方式：JSON
- 要求权限：无，仅登录

| **参数名**  | **描述**     | **是否必须** | **类型** |
|----------|------------|----------|--------|
| faceInfo | Base64人脸图片 | 是        | string |

## 返回值——成功

```json
{
  "code": 0,
  "data": "（faceInfo原样返回）",
  "msg": null
}
```

## 返回值——缺少人脸信息

```json
{
  "code": 1,
  "data": null,
  "msg": "人脸信息缺失"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer your_jwt_token");
myHeaders.append("Content-Type", "application/json");
var raw = JSON.stringify({
    "faceInfo": "base64imagehere..."
});
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/auth/updateFaceInfo", requestOptions)
    .then(response => response.json())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 人脸识别登录

## 接口地址

```bash
/auth/loginByFaceInfo
```

## 传入参数

- 要求鉴权：否
- 请求方式：POST
- 传入方式：JSON
- 要求权限：无

| **参数名**  | **描述**     | **是否必须** | **类型** |
|----------|------------|----------|--------|
| faceInfo | Base64人脸图片 | 是        | string |

## 返回值——成功

```json
{
  "code": 0,
  "data": {
    "access_token": "...",
    "refresh_token": "...",
    "payload": {
      "user": {
        
      },
      "role": [
        
      ],
      "permissions": [
        
      ]
    }
  },
  "msg": "登录成功"
}
```

## 返回值——未识别人脸

```json
{
  "code": 1,
  "data": null,
  "msg": "无法校验人脸"
}
```

## 返回值——缺少人脸信息

```json
{
  "code": 1,
  "data": null,
  "msg": "人脸信息缺失"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
var raw = JSON.stringify({
    "faceInfo": "base64imagehere..."
});
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/auth/loginByFaceInfo", requestOptions)
    .then(response => response.json())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 更新个人信息

## 接口地址

```bash
/auth/updateInfo
```

## 传入参数

- 要求鉴权：是（JWT）
- 请求方式：POST
- 传入方式：JSON
- 要求权限：USER.UPDATE

| **参数名**    | **描述**   | **是否必须** | **类型** |
|------------|----------|----------|--------|
| email      | 邮箱       | 否        | string |
| phone      | 电话号码     | 否        | string |
| name       | 姓名       | 否        | string |
| gender     | 性别       | 否        | string |
| work_years | 工龄       | 否        | int    |
| department | 部门       | 否        | string |
| faceInfo   | 人脸Base64 | 否        | string |

## 返回值——成功

```json
{
  "code": 0,
  "data": {
  },
  "msg": "更新数据成功"
}
```

## 返回值——失败

```json
{
  "code": 1,
  "data": "错误描述",
  "msg": "更新数据失败"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer your_jwt_token");
myHeaders.append("Content-Type", "application/json");
var raw = JSON.stringify({
    "email": "user@example.com",
    "phone": "18000000001",
    "name": "张三",
    "gender": "男",
    "work_years": 5,
    "department": "技术部",
    "faceInfo": "base64string"
});
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/auth/updateInfo", requestOptions)
    .then(response => response.json())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 修改密码

## 接口地址

`/auth/updatePassword`

## 传入参数

- 要求鉴权：是（JWT）
- 请求方式：POST
- 传入方式：JSON
- 要求权限：无，仅登录

| **参数名**     | **描述** | **是否必须** | **类型** |
|-------------|--------|----------|--------|
| password    | 原密码    | 是        | string |
| newPassword | 新密码    | 是        | string |

## 返回值——成功

```json
{
  "code": 0,
  "data": true,
  "msg": "更新密码成功"
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
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer your_jwt_token");
myHeaders.append("Content-Type", "application/json");
var raw = JSON.stringify({
    "password": "oldpass123",
    "newPassword": "newpass456"
});
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/auth/updatePassword", requestOptions)
    .then(response => response.json())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```