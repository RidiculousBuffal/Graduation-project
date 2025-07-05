# **根据字典键获取字典记录**

## **接口地址**

`/dictionary/getDictionary/{dict_key}`

**传入参数**

- 要求鉴权：是
- 请求方式：GET
- 传入方式：路径参数
- 要求权限：DICTIONARY.READ

|**参数名**|**描述**|**是否必须**|**类型**|
|-|-|-|-|
|dict_key|字典键|是|string|


## **返回值——成功**

```json
{
  "code": 0,
  "data": {
    "dict_key": "flight_status",
    "dict_name": "飞行状态",
    "description": "飞机飞行流程状态",
    "parent_key": "status",
    "sort_order": 10,
    "created_at": "2023-11-30T12:00:00",
    "updated_at": "2023-11-30T12:00:00",
    "children": [
      {
        "dict_key": "scheduled",
        "dict_name": "已排班",
        "description": "航班已安排",
        "parent_key": "flight_status",
        "sort_order": 11,
        "created_at": "2023-11-30T12:00:00",
        "updated_at": "2023-11-30T12:00:00",
        "children": []
      },
      {
        "dict_key": "boarding",
        "dict_name": "登机中",
        "description": "开始登机",
        "parent_key": "flight_status",
        "sort_order": 12,
        "created_at": "2023-11-30T12:00:00",
        "updated_at": "2023-11-30T12:00:00",
        "children": []
      }
    ]
  },
  "msg": "获取字典成功"
}
```

## **返回值——未找到**

```json
{
  "code": 1,
  "data": {
    "error": "未找到键为flight_status的字典"
  },
  "msg": "未找到字典"
}
```

## **返回值——参数错误**

```json
{
  "code": 1,
  "data": {
    "error": "字典键不能为空"
  },
  "msg": "无效的字典数据"
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
fetch("http://localhost:5000/api/dictionary/getDictionary/flight_status", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

# **查询某个父字典下的所有子字典**

## **接口地址**

`/dictionary/getChildrenByParentKey/{parent_key}`

## **传入参数**

- 要求鉴权：是
- 请求方式：GET
- 传入方式：路径参数
- 要求权限：DICTIONARY.READ

|**参数名**|**描述**|**是否必须**|**类型**|
|-|-|-|-|
|parent_key|父字典键|是|string|


## **返回值——成功**

```json
{
  "code": 0,
  "data": [
    {
      "dict_key": "scheduled",
      "dict_name": "已排班",
      "description": "航班已安排",
      "parent_key": "flight_status",
      "sort_order": 11,
      "created_at": "2023-11-30T12:00:00",
      "updated_at": "2023-11-30T12:00:00",
      "children": []
    },
    {
      "dict_key": "boarding",
      "dict_name": "登机中",
      "description": "开始登机",
      "parent_key": "flight_status",
      "sort_order": 12,
      "created_at": "2023-11-30T12:00:00",
      "updated_at": "2023-11-30T12:00:00",
      "children": []
    },
    {
      "dict_key": "departed",
      "dict_name": "已起飞",
      "description": "飞机已起飞",
      "parent_key": "flight_status",
      "sort_order": 13,
      "created_at": "2023-11-30T12:00:00",
      "updated_at": "2023-11-30T12:00:00",
      "children": []
    }
  ],
  "msg": "获取子字典成功"
}
```

## **返回值——参数错误**

```json
{
  "code": 1,
  "data": {
    "error": "父字典键不能为空"
  },
  "msg": "无效的字典数据"
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
fetch("http://localhost:5000/api/dictionary/getChildrenByParentKey/flight_status", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

# **分页查询字典记录**

## **接口地址**

`/dictionary/searchDictionary`

## **传入参数**

- 要求鉴权：是
- 请求方式：GET
- 传入方式：query参数
- 要求权限：DICTIONARY.READ

|**参数名**|**描述**|**是否必须**|**类型**|
|-|-|-|-|
|dict_name|字典名称（模糊查询）|否|string|
|parent_key|父字典键|否|string|
|current_page|页码，默认值为1|否|integer|
|page_size|每页数量，默认值为10|否|integer|


## **返回值——成功**

```json
{
  "code": 0,
  "data": {
    "data": [
      {
        "dict_key": "flight_status",
        "dict_name": "飞行状态",
        "description": "飞机飞行流程状态",
        "parent_key": "status",
        "sort_order": 10,
        "created_at": "2023-11-30T12:00:00",
        "updated_at": "2023-11-30T12:00:00",
        "children": [
          {
            "dict_key": "scheduled",
            "dict_name": "已排班",
            "description": "航班已安排",
            "parent_key": "flight_status",
            "sort_order": 11,
            "created_at": "2023-11-30T12:00:00",
            "updated_at": "2023-11-30T12:00:00",
            "children": []
          }
        ]
      }
    ],
    "pagination": {
      "current_page": 1,
      "page_size": 10,
      "total": 1,
      "total_pages": 1
    }
  },
  "msg": "查询字典列表成功"
}
```

## **返回值——参数错误**

```json
{
  "code": 1,
  "data": {
    "error": "页码和每页大小必须大于0"
  },
  "msg": "无效的字典数据"
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
fetch("http://localhost:5000/api/dictionary/searchDictionary?dict_name=状态&parent_key=status&current_page=1&page_size=10", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```