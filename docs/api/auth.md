# 注册接口

## 接口地址

```bash
/auth/register
```

## 传入参数

|参数名|描述|是否必须|
|-|-|-|
|`**username**`|用户名|是|
|`**password**`|密码|是|
|`**email**`|邮箱|否|


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