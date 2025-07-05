# 获得所有工程师

## 接口地址

```bash
/auth/getEngineers
```

## **传入参数**

- 要求鉴权：是
- 请求方式：GET
- 传入方式：无参数
- 要求权限：USER.READ

## 返回值——成功

```json
{
    "code": 0,
    "data": null,
    "msg": [
        {
            "contact_info": null,
            "created_at": "2025-04-01 23:21:39",
            "department": null,
            "email": null,
            "faceInfo": null,
            "gender": null,
            "last_login": null,
            "name": null,
            "phone": null,
            "status": true,
            "updated_at": "2025-04-01 23:21:39",
            "user_id": "3282f685-b6a5-4d27-b6d5-8cf906a86dbd",
            "username": "licheng.zhou5",
            "work_years": null
        },
        {
            "contact_info": null,
            "created_at": "2025-04-01 23:19:53",
            "department": null,
            "email": null,
            "faceInfo": null,
            "gender": null,
            "last_login": null,
            "name": null,
            "phone": null,
            "status": true,
            "updated_at": "2025-04-01 23:19:53",
            "user_id": "7b2c00f2-cb0e-4370-802e-e9b013263120",
            "username": "licheng.zhou3",
            "work_years": null
        },
        {
            "contact_info": null,
            "created_at": "2025-04-01 23:23:23",
            "department": null,
            "email": null,
            "faceInfo": null,
            "gender": null,
            "last_login": null,
            "name": null,
            "phone": null,
            "status": true,
            "updated_at": "2025-04-01 23:23:23",
            "user_id": "7d9c4981-5593-4b35-bb5f-0c4fd35d225b",
            "username": "licheng.zhou6",
            "work_years": null
        },
        {
            "contact_info": null,
            "created_at": "2025-04-01 20:07:23",
            "department": null,
            "email": null,
            "faceInfo": null,
            "gender": null,
            "last_login": null,
            "name": null,
            "phone": null,
            "status": false,
            "updated_at": "2025-04-01 20:07:23",
            "user_id": "82294790-235f-424a-9b85-ba01b66e55b5",
            "username": "licheng.zhou1",
            "work_years": null
        }
    ]
}
```

## 请求示例:

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0ODYxMjM5MiwianRpIjoiMTExMWJmYTAtYmRjMS00Njk5LTkxMzAtYmQ0NGIyNTc5MWQ1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0ODYxMjM5MiwiY3NyZiI6ImQ1NmJkNmEyLWZjNDEtNDJmOC1iYjUzLTA5MWUzMzc2NDgxYSIsImV4cCI6MTc0ODY5ODc5Mn0.d8PCAmnh_L8ijrs20DJrDB3Uv3Rb-ERx3dDQwlwjyws");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var requestOptions = {
   method: 'GET',
   headers: myHeaders,
   redirect: 'follow'
};
fetch("http://localhost:5000/api/auth/getEngineers", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```