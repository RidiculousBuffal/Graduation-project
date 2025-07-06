# 创建航站楼

:::info
本毕业设计中默认航站楼=机场
:::

## 接口地址

```Bash
/terminal/createTerminal
```

## 传入参数

要求鉴权:是

请求方式:`POST`

传入方式:`json`

要求权限:`TERMINAL.ADD`

| 参数名                 | 描述   | 是否必须 | 类型       |
|---------------------|------|------|----------|
| `**terminal_name**` | 机场名字 | 是    | `string` |
| `**description**`   | 描述   | 否    | `string` |

## 返回值——成功

```JSON
{
  "code": 0,
  "data": {
    "description": "测试航站楼10",
    "terminal_id": "0f78d109-f1cd-4ffb-9099-5371960ea9eb",
    "terminal_name": "航站楼10"
  },
  "msg": "添加航站楼成功"
}
```

## 返回值——已经存在

```JSON
{
  "code": 1,
  "data": null,
  "msg": "航站楼名称已存在"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTEyNzI1NCwianRpIjoiMjk4MTM3ZTUtZWRmOS00ZWYyLTlhY2EtNDllN2YwYTZhMjc5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NTEyNzI1NCwiY3NyZiI6IjU0NmEyMWI0LWYyY2QtNGQ3OC1iZGYxLWE5YmVmMWYyOGY0ZCIsImV4cCI6MTc0NTIxMzY1NH0.8fZIwcWjVk4fFL_hSVUibjZB1KkpSYN4-tHP8AWTYk4");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var raw = JSON.stringify({
    "terminal_name": "航站楼10",
    "description": "测试航站楼10"
});
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/terminal/createTerminal", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 根据航站楼ID获得详细信息

## **接口地址**

`/terminal/getTerminal/{terminal_id}`

## **传入参数**

- 要求鉴权：是
- 请求方式：GET
- 传入方式：路径参数
- 要求权限：TERMINAL.READ

| **参数名**     | **描述** | **是否必须** | **类型** |
|-------------|--------|----------|--------|
| terminal_id | 航站楼ID  | 是        | string |

## **返回值——成功**

```JSON
{
  "code": 0,
  "data": {
    "terminal_id": "0f78d109-f1cd-4ffb-9099-5371960ea9eb",
    "terminal_name": "航站楼10",
    "description": "测试航站楼10"
  },
  "msg": "获取航站楼成功"
}
```

## **返回值——未找到**

```JSON
{
  "code": 1,
  "data": {
    "error": "未找到ID为0f78d109-f1cd-4ffb-9099-5371960ea9eb的航站楼"
  },
  "msg": "航站楼未找到"
}
```

## **请求示例**

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTEyNzI1NCwianRpIjoiMjk4MTM3ZTUtZWRmOS00ZWYyLTlhY2EtNDllN2YwYTZhMjc5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NTEyNzI1NCwiY3NyZiI6IjU0NmEyMWI0LWYyY2QtNGQ3OC1iZGYxLWE5YmVmMWYyOGY0ZCIsImV4cCI6MTc0NTIxMzY1NH0.8fZIwcWjVk4fFL_hSVUibjZB1KkpSYN4-tHP8AWTYk4");
var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/terminal/getTerminal/0f78d109-f1cd-4ffb-9099-5371960ea9eb", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 更新航站楼

## **接口地址**

`/terminal/updateTerminal/{terminal_id}`

## **传入参数**

- 要求鉴权：是
- 请求方式：POST
- 传入方式：json
- 要求权限：TERMINAL.UPDATE

| **参数名**       | **描述**      | **是否必须** | **类型** |
|---------------|-------------|----------|--------|
| terminal_id   | 航站楼ID（路径参数） | 是        | string |
| terminal_name | 航站楼名称       | 否        | string |
| description   | 描述          | 否        | string |

## **返回值——成功**

```JSON
{
  "code": 0,
  "data": {
    "terminal_id": "0f78d109-f1cd-4ffb-9099-5371960ea9eb",
    "terminal_name": "航站楼10更新",
    "description": "测试航站楼10更新"
  },
  "msg": "更新航站楼成功"
}
```

## **返回值——名称已存在**

```JSON
{
  "code": 1,
  "data": null,
  "msg": "航站楼名称已存在"
}
```

## **返回值——未找到**

```JSON
{
  "code": 1,
  "data": {
    "error": "未找到ID为0f78d109-f1cd-4ffb-9099-5371960ea9eb的航站楼或更新失败"
  },
  "msg": "更新航站楼失败"
}
```

## **请求示例**

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTEyNzI1NCwianRpIjoiMjk4MTM3ZTUtZWRmOS00ZWYyLTlhY2EtNDllN2YwYTZhMjc5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NTEyNzI1NCwiY3NyZiI6IjU0NmEyMWI0LWYyY2QtNGQ3OC1iZGYxLWE5YmVmMWYyOGY0ZCIsImV4cCI6MTc0NTIxMzY1NH0.8fZIwcWjVk4fFL_hSVUibjZB1KkpSYN4-tHP8AWTYk4");
myHeaders.append("Content-Type", "application/json");
var raw = JSON.stringify({
    "terminal_name": "航站楼10更新",
    "description": "测试航站楼10更新"
});
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/terminal/updateTerminal/0f78d109-f1cd-4ffb-9099-5371960ea9eb", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 删除航站楼

## **接口地址**

`/terminal/deleteTerminal/{terminal_id}`

## **传入参数**

- 要求鉴权：是
- 请求方式：DELETE
- 传入方式：路径参数
- 要求权限：TERMINAL.DELETE

| **参数名**     | **描述** | **是否必须** | **类型** |
|-------------|--------|----------|--------|
| terminal_id | 航站楼ID  | 是        | string |

## **返回值——成功**

```JSON
{
  "code": 0,
  "data": null,
  "msg": "删除航站楼成功"
}
```

## **返回值——未找到**

```JSON
{
  "code": 1,
  "data": {
    "error": "未找到ID为0f78d109-f1cd-4ffb-9099-5371960ea9eb的航站楼或删除失败"
  },
  "msg": "删除航站楼失败"
}
```

## **请求示例**

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTEyNzI1NCwianRpIjoiMjk4MTM3ZTUtZWRmOS00ZWYyLTlhY2EtNDllN2YwYTZhMjc5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NTEyNzI1NCwiY3NyZiI6IjU0NmEyMWI0LWYyY2QtNGQ3OC1iZGYxLWE5YmVmMWYyOGY0ZCIsImV4cCI6MTc0NTIxMzY1NH0.8fZIwcWjVk4fFL_hSVUibjZB1KkpSYN4-tHP8AWTYk4");
var requestOptions = {
    method: 'DELETE',
    headers: myHeaders,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/terminal/deleteTerminal/0f78d109-f1cd-4ffb-9099-5371960ea9eb", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 分页查询航站楼

## **接口地址**

`/terminal/searchTerminal`

## **传入参数**

- 要求鉴权：是
- 请求方式：GET
- 传入方式：-query参数
- 要求权限：TERMINAL.READ

| **参数名**       | **描述**      | **是否必须** | **类型**  |
|---------------|-------------|----------|---------|
| terminal_name | 航站楼名称（模糊查询） | 否        | string  |
| current_page  | 页码，默认值为1    | 否        | integer |
| page_size     | 每页数量，默认值为10 | 否        | integer |

## **返回值——成功**

```JSON
{
  "code": 0,
  "data": {
    "data": [
      {
        "terminal_id": "0f78d109-f1cd-4ffb-9099-5371960ea9eb",
        "terminal_name": "航站楼10",
        "description": "测试航站楼10"
      }
    ],
    "pagination": {
      "total": 1,
      "current_page": 1,
      "page_size": 10
    }
  },
  "msg": "查询航站楼成功"
}
```

## **返回值——参数错误**

```JSON
{
  "code": 1,
  "data": {
    "error": "页码和每页大小必须大于0"
  },
  "msg": "参数错误"
}
```

## **请求示例**

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTEyNzI1NCwianRpIjoiMjk4MTM3ZTUtZWRmOS00ZWYyLTlhY2EtNDllN2YwYTZhMjc5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NTEyNzI1NCwiY3NyZiI6IjU0NmEyMWI0LWYyY2QtNGQ3OC1iZGYxLWE5YmVmMWYyOGY0ZCIsImV4cCI6MTc0NTIxMzY1NH0.8fZIwcWjVk4fFL_hSVUibjZB1KkpSYN4-tHP8AWTYk4");
var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/terminal/searchTerminal?terminal_name=航站楼&current_page=1&page_size=10", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```