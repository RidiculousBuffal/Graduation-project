# 登录接口

## 接口地址

```bash
/auth/login
```

## 传入参数

| 参数名            | 描述  | 是否必须 |
|----------------|-----|------|
| `**username**` | 用户名 | 是    |
| `**password**` | 密码  | 是    |

传入方式:`json`

Method:`POST`

## 返回值——登录成功

返回示例如下:

在`data`字段中返回`access_token`(后续校验用),`payload`载荷中为:用户角色,用户权限(已经去重),用户基本信息,`refresh_token`
用于刷新令牌

```json
{
  "code": 0,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDA4OTI3NiwianRpIjoiMDhkNWFkZWEtNjMwOC00YmJmLTk1ZGUtYzAxMDI4YTQxNTFmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVjNjUxYTc4LTQ3YzctNGM4Ny1hZjVlLWExNjI4NjQxZWM5OCIsIm5iZiI6MTc0NDA4OTI3NiwiY3NyZiI6IjQ4NTBmMWQ2LWIzYWYtNDQ0MC1hNjA1LTNhM2UwZjcyMGZhZiIsImV4cCI6MTc0NDE3NTY3Nn0.1a_Jj1oy8FGA_4L1FQku5z0ZZoz8NyHDzm5Yfowz-8Y",
    "payload": {
      "permissions": [
        {
          "description": "测试权限",
          "permission_id": 1,
          "permission_name": "test_permission"
        }
      ],
      "role": [
        {
          "description": "普通用户",
          "role_id": 2,
          "role_name": "USER"
        }
      ],
      "user": {
        "created_at": "2025-04-08 13:14:30",
        "email": null,
        "faceInfo": null,
        "last_login": "2025-04-08 13:14:37",
        "phone": null,
        "status": true,
        "updated_at": "2025-04-08 13:14:30",
        "user_id": "ec651a78-47c7-4c87-af5e-a1628641ec98",
        "username": "licheng.zhou"
      }
    },
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDA4OTI3NiwianRpIjoiZmYwM2JiOWYtZjVhYy00NmRkLWI5YTctODUwNmNkZjk3MjU0IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJlYzY1MWE3OC00N2M3LTRjODctYWY1ZS1hMTYyODY0MWVjOTgiLCJuYmYiOjE3NDQwODkyNzYsImNzcmYiOiJmYTc3MzFjZS1lOWZkLTRlYmEtOWQ2NS04MTRhNWJmNzViMmUiLCJleHAiOjE3NDY2ODEyNzZ9.e2EsW6mAJ9DZFH7Eta649iRTlqmPfBZaRrK6epzUjr8"
  },
  "msg": "登录成功"
}
```

## 返回值——登录失败

```json
{
  "code": 1,
  "data": null,
  "msg": "登录失败"
}
```

## 返回值——用户被禁用

```json
{
  "code": 1,
  "data": null,
  "msg": "账号被禁用"
}
```

## 返回值——缺少参数

```json
{
  "code": 1,
  "data": null,
  "msg": "用户名密码不能为空"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
var raw = JSON.stringify({
    "username": "licheng.zhou9",
    "password": "Zhougezuishuai22"
});
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/auth/login", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 注册接口

## 接口地址

```bash
/auth/register
```

## 传入参数

| 参数名            | 描述  | 是否必须 |
|----------------|-----|------|
| `**username**` | 用户名 | 是    |
| `**password**` | 密码  | 是    |
| `**email**`    | 邮箱  | 否    |

传入方式:`json`

Method:`POST`

## 返回值——注册成功

```JSON
{
  "code": 0,
  "data": null,
  "msg": "注册成功"
}
```

## 返回值——用户被使用

```JSON
{
  "code": 1,
  "data": null,
  "msg": "用户名已存在"
}
```

## 返回值——缺少参数

```JSON
{
  "code": 1,
  "data": null,
  "msg": "用户名密码不能为空"
}
```

## 返回值——邮箱已存在

```JSON
{
  "code": 1,
  "data": null,
  "msg": "邮箱已经存在"
}
```

## 请求示例

```javascript
var myHeaders = new Headers();
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var raw = JSON.stringify({
    "username": "licheng.zhou334",
    "password": "Zhougezuishuai22",
    "email": "licheng.zhou@cat1hay.fr"
});
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/auth/register", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 刷新令牌

## 接口地址

```bash
/auth/refresh
```

## 传入参数

**请求头:**

```bash
Authorization: Bearer {JWT_REFRESH_TOKEN}
```

## 返回值——刷新成功

```JSON
{
  "code": 0,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDA4OTUzMSwianRpIjoiM2RlMDIyOWUtODNjNi00NDI4LTlhYTAtYmZhY2Q3NGJjZTU1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVjNjUxYTc4LTQ3YzctNGM4Ny1hZjVlLWExNjI4NjQxZWM5OCIsIm5iZiI6MTc0NDA4OTUzMSwiY3NyZiI6ImI3YWMxMWMyLWI3OTMtNDlkOS1hNzM2LWM3ZDJmNzgwMTBkNiIsImV4cCI6MTc0NDE3NTkzMX0.PwYnMkSXQCNLnjMriludb0isVXxezMOmp7r5t6NpQDU"
  },
  "msg": "刷新令牌成功"
}
```

## 返回值——未携带token

**状态码:401**

```JSON
{
  "msg": "Missing Authorization Header"
}
```

## 返回值——token异常

**状态码:422**

```JSON
{
  "msg": "Invalid header string: Expecting ',' delimiter: line 1 column 15 (char 14)"
}
```