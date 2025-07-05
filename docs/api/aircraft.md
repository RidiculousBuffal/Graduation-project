# 新增飞机

## 接口地址

```bash
/aircraft/createAircraft
```

## 传入参数

要求鉴权:是

请求方式:`POST`

传入方式:`json`

要求权限:`AIRCRAFT.ADD`

|参数名|描述|是否必须|
|-|-|-|
|`**aircraft_name**`|飞机名|是|
|`typeid`|飞机类型ID|是|
|`age`|飞机年龄|否|


## 返回值——成功

```JSON
{
    "code": 0,
    "data": {
        "age": 10,
        "aircraft_id": "a468b3a7-46b6-485f-80be-3c518995f7e7",
        "aircraft_name": "测试飞机2",
        "type_description": "A short- to medium-range twinjet narrow-body airliner.",
        "type_name": "Boeing 737",
        "typeid": "TYPE001"
    },
    "msg": "添加飞机成功"
}
```

## 返回值——无权限

```JSON
{
  "code": 1,
  "data": null,
  "msg": "权限校验失败,要求权限:['AIRCRAFT.ADD']"
}
```

## 返回值——typeId不存在

```JSON
{
  "code": 1,
  "data": {
    "error": "(MySQLdb.IntegrityError) (1452, 'Cannot add or update a child row: a foreign key constraint fails (`dhu_aircraft`.`aircraft`, CONSTRAINT `aircraft_ibfk_1` FOREIGN KEY (`typeid`) REFERENCES `aircraft_type` (`typeid`))')\n[SQL: INSERT INTO aircraft (aircraft_id, aircraft_name, age, typeid) VALUES (%s, %s, %s, %s)]\n[parameters: ('2b31a556-40b3-4f73-81cc-51665070dc52', '测试飞机', 10, 'TYPE031')]\n(Background on this error at: https://sqlalche.me/e/20/gkpj)"
  },
  "msg": "飞机类型信息未找到"
}
```

## 返回值——参数缺少

```JSON
{
  "code": 1,
  "data": "1 validation error for AircraftCreateDTO\ntypeid\n  Field required [type=missing, input_value={'aircraft_name': '测试飞机', 'age': 10}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.11/v/missing",
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
   "aircraft_name": "测试飞机2",
   "typeid": "TYPE001",
   "age": 10
});
var requestOptions = {
   method: 'POST',
   headers: myHeaders,
   body: raw,
   redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/createAircraft", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```

# 获取飞机详细信息

## 接口地址

```bash
/aircraft/getAircraft/<飞机ID>
```

**示例:**

```bash
/aircraft/getAircraft/a468b3a7-46b6-485f-80be-3c518995f7e7
```

## 传入参数

要求鉴权:是

请求方式:`GET`

传入方式:`json`

要求权限:`AIRCRAFT.READ`

**直接在路径后加上飞机的id即可**

## 返回值——查询成功

```JSON
{
  "code": 0,
  "data": {
    "age": 10,
    "aircraft_id": "a468b3a7-46b6-485f-80be-3c518995f7e7",
    "aircraft_name": "测试飞机2",
    "type_description": "A short- to medium-range twinjet narrow-body airliner.",
    "type_name": "Boeing 737",
    "typeid": "TYPE001"
  },
  "msg": "获取飞机信息成功"
}
```

## 返回值——记录不存在

```JSON
{
  "code": 1,
  "data": {
    "error": "未找到ID为a468b3a7-46b6-485f-80be-3c5189957的飞机"
  },
  "msg": "飞机信息未找到"
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
fetch("http://localhost:5000/api/aircraft/getAircraft/a468b3a7-46b6-485f-80be-3c518995f7e7", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```

# 更新飞机

## 接口地址

```bash
/aircraft/updateAircraft/<飞机ID>
```

## 传入参数

要求鉴权:是

请求方式:`POST`

传入方式:`json`

要求权限:`AIRCRAFT_UPDATE`

|参数名|描述|是否必须|
|-|-|-|
|`**aircraft_name**`|飞机名|是|
|`typeid`|飞机类型ID|是|
|`age`|飞机年龄|否|


## 返回值——成功

```JSON
{
  "code": 0,
  "data": {
    "age": 11,
    "aircraft_id": "AC004",
    "aircraft_name": "更新飞机信息",
    "type_description": "A short- to medium-range, narrow-body, commercial passenger twin-engine jet airliner.",
    "type_name": "Airbus A320",
    "typeid": "TYPE002"
  },
  "msg": "更新飞机成功"
}
```

## 返回值——更新的飞机类型不存在

```JSON
{
  "code": 1,
  "data": {
    "error": "(MySQLdb.IntegrityError) (1452, 'Cannot add or update a child row: a foreign key constraint fails (`dhu_aircraft`.`aircraft`, CONSTRAINT `aircraft_ibfk_1` FOREIGN KEY (`typeid`) REFERENCES `aircraft_type` (`typeid`))')\n[SQL: UPDATE aircraft SET aircraft_name=%s, age=%s, typeid=%s WHERE aircraft.aircraft_id = %s]\n[parameters: ('更新飞机信息', 11, 'TYPE1002', 'AC001')]\n(Background on this error at: https://sqlalche.me/e/20/gkpj)"
  },
  "msg": "飞机类型信息未找到"
}
```

## 返回值——更新的飞机ID不存在

```JSON
{
  "code": 1,
  "data": {
    "error": "未找到ID为AC0044的飞机或更新失败"
  },
  "msg": "更新飞机失败"
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
   "aircraft_name": "更新飞机信息",
   "typeid": "TYPE002",
   "age": 11
});
var requestOptions = {
   method: 'POST',
   headers: myHeaders,
   body: raw,
   redirect: 'follow'
};
fetch("http://localhost:5000/api/aircraft/updateAircraft/AC004", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```

# 删除飞机

## 接口地址

```bash
/aircraft/deleteAircraft/<飞机ID>
```

## 传入参数

要求鉴权:是

请求方式:`DELETE`

传入方式:`地址参数`

要求权限:`AIRCRAFT_DELETE`

## 返回值——删除成功

```JSON
{
  "code": 0,
  "data": null,
  "msg": "删除飞机成功"
}
```

## 返回值——飞机不存在

```JSON
{
  "code": 1,
  "data": {
    "error": "未找到ID为AC004的飞机或删除失败"
  },
  "msg": "删除飞机失败"
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
fetch("http://localhost:5000/api/aircraft/deleteAircraft/AC004", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```

# 分页查询飞机

## 说明

:::warning
本接口是分页查询,默认按照`aircraft_name`升序排列,不传分页参数则默认是查询第`1`页的`10`条记录
:::

## 接口地址

```bash
/aircraft/searchAircraft
```

## 传入参数

要求鉴权:是

请求方式:`GET`

传入方式:`QUERY`

要求权限:`AIRCRAFT_READ`

|参数名|描述|是否必须|
|-|-|-|
|`**aircraft_name**`|飞机名|否|
|`**aircraft_type_name**`|飞机类型名|否|
|`**aircraft_age**`|飞机年龄|否|
|**current_page**|当前页数|否|
|`**page_size**`|每页展示条数|否|


## 返回值——查询成功

```JSON
{
  "code": 0,
  "data": {
    "data": [
      {
        "age": 7,
        "aircraft_id": "AC005",
        "aircraft_name": "Eagle Epsilon",
        "type_description": "A short- to medium-range twinjet narrow-body airliner.",
        "type_name": "Boeing 737",
        "typeid": "TYPE001"
      },
      {
        "age": 5,
        "aircraft_id": "AC001",
        "aircraft_name": "Flight Alpha",
        "type_description": "A short- to medium-range twinjet narrow-body airliner.",
        "type_name": "Boeing 737",
        "typeid": "TYPE001"
      },
      {
        "age": 3,
        "aircraft_id": "AC002",
        "aircraft_name": "Sky Beta",
        "type_description": "A short- to medium-range, narrow-body, commercial passenger twin-engine jet airliner.",
        "type_name": "Airbus A320",
        "typeid": "TYPE002"
      },
      {
        "age": 1,
        "aircraft_id": "AC008",
        "aircraft_name": "Storm Theta",
        "type_description": "A regional jet used for short-haul flights with a capacity of up to 88 passengers.",
        "type_name": "Embraer E175",
        "typeid": "TYPE005"
      },
      {
        "age": 8,
        "aircraft_id": "AC007",
        "aircraft_name": "Thunder Eta",
        "type_description": "A wide-body commercial jet airliner, often referred to as the \"Jumbo Jet\".",
        "type_name": "Boeing 747",
        "typeid": "TYPE003"
      },
      {
        "age": 4,
        "aircraft_id": "AC006",
        "aircraft_name": "Wings Zeta",
        "type_description": "A short- to medium-range, narrow-body, commercial passenger twin-engine jet airliner.",
        "type_name": "Airbus A320",
        "typeid": "TYPE002"
      },
      {
        "age": 11,
        "aircraft_id": "AC003",
        "aircraft_name": "更新飞机信息",
        "type_description": "A short- to medium-range, narrow-body, commercial passenger twin-engine jet airliner.",
        "type_name": "Airbus A320",
        "typeid": "TYPE002"
      },
      {
        "age": 10,
        "aircraft_id": "3f6f0da9-e386-4727-9ac0-765977b6db3d",
        "aircraft_name": "测试飞机",
        "type_description": "A short- to medium-range twinjet narrow-body airliner.",
        "type_name": "Boeing 737",
        "typeid": "TYPE001"
      },
      {
        "age": 10,
        "aircraft_id": "d3c71f3c-f9ea-46d7-90cd-06a80dc5831a",
        "aircraft_name": "测试飞机",
        "type_description": "A short- to medium-range twinjet narrow-body airliner.",
        "type_name": "Boeing 737",
        "typeid": "TYPE001"
      },
      {
        "age": 10,
        "aircraft_id": "e763a6db-45a3-42e0-bbd3-57ff5c324642",
        "aircraft_name": "测试飞机",
        "type_description": "A short- to medium-range twinjet narrow-body airliner.",
        "type_name": "Boeing 737",
        "typeid": "TYPE001"
      }
    ],
    "pagination": {
      "current_page": 1,
      "page_size": 10,
      "total": 11,
      "total_pages": 2
    }
  },
  "msg": "查询飞机列表成功"
}
```

## 返回值——没用内容时

```JSON
{
  "code": 0,
  "data": {
    "data": [],
    "pagination": {
      "current_page": 1,
      "page_size": 10,
      "total": 0,
      "total_pages": 0
    }
  },
  "msg": "查询飞机列表成功"
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
fetch("http://localhost:5000/api/aircraft/searchAircraft?aircraft_name=%E6%B5%8B%E8%AF%95%E9%A3%9E%E6%9C%BA&aircraft_age=10&aircraft_type_name=1Boeing%20737", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```

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
fetch("http://localhost:5000/api/aircraft/searchAircraft?current_page=2&page_size=5", requestOptions)
   .then(response => response.text())
   .then(result => console.log(result))
   .catch(error => console.log('error', error));
```