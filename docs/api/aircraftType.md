# 创建一个新的飞机类型

## 接口地址

```bash
/aircraft/createAircraftType
```

## 传入参数

要求鉴权:是

请求方式:`POST`

传入方式:`JSON`

要求权限:`AIRCRAFT_TYPE_ADD`

| 参数名             | 描述  | 是否必须 |
|-----------------|-----|------|
| `**type_name**` | 类型名 | 是    |
| `description`   | 描述  | 否    |

## 返回值——成功

```JSON
{
  "code": 0,
  "data": {
    "description": "测试类型123",
    "type_name": "测试类型12345",
    "typeid": "f1f6a88d-a13f-4bd2-8ca0-237f24b17859"
  },
  "msg": "添加飞机类型成功"
}
```

## 返回值——类型重复

```JSON
{
  "code": 1,
  "data": null,
  "msg": "飞机类型已存在"
}
```

## 返回值——类型名缺少

```JSON
{
  "code": 1,
  "data": "1 validation error for AircraftTypeCreateDTO\ntype_name\n  Field required [type=missing, input_value={'description': '测试类型123'}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.11/v/missing",
  "msg": "参数缺失"
}
```

## 请求示例

```javascript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDQzMTIzNiwianRpIjoiZDY1NTAyODQtNzE3ZS00MzYwLWIzYjYtZjJiZmVhNzU3NTU1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDQzMTIzNiwiY3NyZiI6ImY5MDYzZmY1LTU1NTctNDc1Yi05OTM2LWIyOTg5NWQ1NDVjOSIsImV4cCI6MTc0NDUxNzYzNn0.QYumiRWIdvjpGtUoZO3iRlyYf-d9ZUaD1D42qk7fdqI");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var raw = JSON.stringify({
    "type_name": "测试类型12345",
    "description": "测试类型123"
});
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/createAircraftType", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 获得飞机类型详细信息

## 接口地址

```bash
/aircraft/getAircraftType/<TypeId>
```

## 传入参数

要求鉴权:是

请求方式:`GET`

传入方式:`地址参数`

要求权限:`AIRCRAFT_TYPE_READ`

## 返回值——获得成功

```JSON
{
  "code": 0,
  "data": {
    "description": "A regional jet used for short-haul flights with a capacity of up to 88 passengers.",
    "type_name": "Embraer E175",
    "typeid": "TYPE005"
  },
  "msg": "获取飞机类型信息成功"
}
```

## 返回值——记录不存在

```JSON
{
  "code": 1,
  "data": {
    "error": "未找到ID为TYPE0051的飞机类型"
  },
  "msg": "飞机类型信息未找到"
}
```

## 请求示例

```javascript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDQzMTIzNiwianRpIjoiZDY1NTAyODQtNzE3ZS00MzYwLWIzYjYtZjJiZmVhNzU3NTU1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDQzMTIzNiwiY3NyZiI6ImY5MDYzZmY1LTU1NTctNDc1Yi05OTM2LWIyOTg5NWQ1NDVjOSIsImV4cCI6MTc0NDUxNzYzNn0.QYumiRWIdvjpGtUoZO3iRlyYf-d9ZUaD1D42qk7fdqI");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/getAircraftType/TYPE0051", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 更新飞机类型详细信息

## 接口地址

```bash
/aircraft/updateAircraftType/<aircraft_type_id>
```

## 传入参数

要求鉴权:是

请求方式:`POST`

传入方式:`地址参数+json`

要求权限:`AIRCRAFT_TYPE_UPDATE`

| 参数名             | 描述  | 是否必须 |
|-----------------|-----|------|
| `**type_name**` | 类型名 | 否    |
| `description`   | 描述  | 否    |

## 返回值——修改成功

```JSON
{
  "code": 0,
  "data": {
    "description": "update1231322131123",
    "type_name": "更新后12345",
    "typeid": "TYPE004"
  },
  "msg": "更新飞机类型成功"
}
```

## 返回值——名字和别的重复

```JSON
{
  "code": 1,
  "data": null,
  "msg": "飞机类型已存在"
}
```

## 返回值——ID不正确

```JSON
{
  "code": 1,
  "data": {
    "error": "未找到ID为23的飞机类型或更新失败"
  },
  "msg": "更新飞机类型失败"
}
```

## 请求示例

```javascript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDQzMTIzNiwianRpIjoiZDY1NTAyODQtNzE3ZS00MzYwLWIzYjYtZjJiZmVhNzU3NTU1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDQzMTIzNiwiY3NyZiI6ImY5MDYzZmY1LTU1NTctNDc1Yi05OTM2LWIyOTg5NWQ1NDVjOSIsImV4cCI6MTc0NDUxNzYzNn0.QYumiRWIdvjpGtUoZO3iRlyYf-d9ZUaD1D42qk7fdqI");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var raw = JSON.stringify({
    "description": "update1231322131123"
});
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/updateAircraftType/TYPE004", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 删除飞机类型

## 接口地址

```bash
/aircraft/deleteAircraftType/<type_id>
```

## 传入参数

要求鉴权:是

请求方式:`DELETE`

传入方式:`地址参数`

要求权限:`AIRCRAFT_TYPE_DELETE`

## 返回值——删除成功

```JSON
{
  "code": 0,
  "data": null,
  "msg": "删除飞机类型成功"
}
```

## 返回值——删除失败

```JSON
{
  "code": 1,
  "data": {
    "error": "未找到ID为TYPE001的飞机类型或删除失败"
  },
  "msg": "删除飞机类型失败"
}
```

## 请求示例

```javascript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDQzMTIzNiwianRpIjoiZDY1NTAyODQtNzE3ZS00MzYwLWIzYjYtZjJiZmVhNzU3NTU1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDQzMTIzNiwiY3NyZiI6ImY5MDYzZmY1LTU1NTctNDc1Yi05OTM2LWIyOTg5NWQ1NDVjOSIsImV4cCI6MTc0NDUxNzYzNn0.QYumiRWIdvjpGtUoZO3iRlyYf-d9ZUaD1D42qk7fdqI");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var requestOptions = {
    method: 'DELETE',
    headers: myHeaders,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/deleteAircraftType/TYPE001", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

# 飞机类型分页查询

## 接口地址

```bash
/aircraft/searchAircraftType
```

## 传入参数

要求鉴权:是

请求方式:`GET`

传入方式:`QUERY`

要求权限:`AIRCRAFT_TYPE_READ`

| 参数名              | 描述     | 是否必须 |
|------------------|--------|------|
| `**type_name**`  | 飞机类型名  | 否    |
| **current_page** | 当前页数   | 否    |
| `**page_size**`  | 每页展示条数 | 否    |

## 返回值——成功

```JSON
{
  "code": 0,
  "data": {
    "data": [
      {
        "description": "A short- to medium-range, narrow-body, commercial passenger twin-engine jet airliner.",
        "type_name": "Airbus A320",
        "typeid": "TYPE002"
      },
      {
        "description": "A wide-body commercial jet airliner, often referred to as the \"Jumbo Jet\".",
        "type_name": "Boeing 747",
        "typeid": "TYPE003"
      },
      {
        "description": "A regional jet used for short-haul flights with a capacity of up to 88 passengers.",
        "type_name": "Embraer E175",
        "typeid": "TYPE005"
      },
      {
        "description": "update1231322131123",
        "type_name": "更新后12345",
        "typeid": "TYPE004"
      },
      {
        "description": "测试类型123",
        "type_name": "测试类型123",
        "typeid": "c5c18a9b-f8d6-42bf-891e-9e1067deb769"
      },
      {
        "description": "测试类型123",
        "type_name": "测试类型12345",
        "typeid": "f1f6a88d-a13f-4bd2-8ca0-237f24b17859"
      }
    ],
    "pagination": {
      "current_page": 1,
      "page_size": 10,
      "total": 6,
      "total_pages": 1
    }
  },
  "msg": "查询飞机类型列表成功"
}
```

## 请求示例

```javascript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDQzMTIzNiwianRpIjoiZDY1NTAyODQtNzE3ZS00MzYwLWIzYjYtZjJiZmVhNzU3NTU1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NDQzMTIzNiwiY3NyZiI6ImY5MDYzZmY1LTU1NTctNDc1Yi05OTM2LWIyOTg5NWQ1NDVjOSIsImV4cCI6MTc0NDUxNzYzNn0.QYumiRWIdvjpGtUoZO3iRlyYf-d9ZUaD1D42qk7fdqI");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "localhost:5000");
myHeaders.append("Connection", "keep-alive");
var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/searchAircraftType?type_name=&current_page=1", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```