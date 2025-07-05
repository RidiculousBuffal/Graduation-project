# 创建航班

## **接口地址**

`/flight/createFlight`

**传入参数**

- 要求鉴权：`是`
- 请求方式：`POST`
- 传入方式：`json`
- 要求权限：`FLIGHT.ADD`

:::tip
1. 使用 `new Date(timestamp)` 将时间戳转换为 `Date` 对象。
2. 使用 `Date` 对象的 `toISOString()` 方法获取 ISO 格式的字符串（例如 `2025-04-25T00:00:00.000Z`）。
3. 根据需要截取或格式化字符串，得到 `2025-04-25T00:00:00` 格式
:::

| **参数名**               | **描述**              | **是否必须** | **类型**                                 |
|-----------------------|---------------------|----------|----------------------------------------|
| `aircraft_id`         | 飞机ID                | 是        | string                                 |
| `terminal_id`         | 航站楼ID               | 否        | string                                 |
| `estimated_departure` | 预计起飞时间              | 否        | datetime (ISO格式)  如2025-04-25T00:00:00 |
| `estimated_arrival`   | 预计到达时间              | 否        | datetime (ISO格式)                       |
| `flight_status`       | 航班状态，默认值"scheduled" | 否        | string                                 |
| `actual_departure`    | 实际起飞时间              | 否        | datetime (ISO格式)                       |
| `actual_arrival`      | 实际到达时间              | 否        | datetime (ISO格式)                       |
| `health_status`       | 健康状态，默认值"healthy"   | 否        | string                                 |
| `approval_status`     | 审批状态，默认值"pending"   | 否        | string                                 |


## **返回值——成功**


:::tip
`**new Date(this.dateString)**` : JavaScript 的 `Date` 对象可以直接解析这种标准的日期字符串（如 `Sun, 20 Apr 2025 18:09:09 GMT`），并将其转换为 `Date` 对象
:::

```json
{
  "code": 0,
  "data": {
    "actual_arrival": "Sun, 27 Apr 2025 10:00:00 GMT",
    "actual_departure": "Fri, 25 Apr 2025 00:00:00 GMT",
    "aircraft_id": "AC002",
    "approval_status": "pending",
    "created_at": "Sun, 20 Apr 2025 18:09:09 GMT",
    "estimated_arrival": "Sun, 27 Apr 2025 10:00:00 GMT",
    "estimated_departure": "Fri, 25 Apr 2025 00:00:00 GMT",
    "flight_id": "9a29589d-f852-4675-89dc-d7282f3e5a45",
    "flight_status": "cancelled",
    "health_status": "healthy",
    "terminal_id": "244b6279-69d0-4397-b0d8-ef47ceda4e37",
    "updated_at": "Sun, 20 Apr 2025 18:09:09 GMT"
  },
  "msg": "添加航班成功"
}
```

## **返回值——参数错误**

```json
{
  "code": 1,
  "data": {
    "error": "飞机ID不能为空"
  },
  "msg": "航班数据无效"
}
```

## **返回值——时间冲突**

```json
{
  "code": 1,
  "data": {
    "error": "同一飞机在该时间段内已被安排其他航班"
  },
  "msg": "时间冲突错误"
}
```

## **请求示例**

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTEyNzI1NCwianRpIjoiMjk4MTM3ZTUtZWRmOS00ZWYyLTlhY2EtNDllN2YwYTZhMjc5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NTEyNzI1NCwiY3NyZiI6IjU0NmEyMWI0LWYyY2QtNGQ3OC1iZGYxLWE5YmVmMWYyOGY0ZCIsImV4cCI6MTc0NTIxMzY1NH0.8fZIwcWjVk4fFL_hSVUibjZB1KkpSYN4-tHP8AWTYk4");
myHeaders.append("Content-Type", "application/json");
var raw = JSON.stringify({
  "aircraft_id": "aircraft123",
  "terminal_id": "terminal456",
  "estimated_departure": "2023-12-01T08:00:00",
  "estimated_arrival": "2023-12-01T10:00:00",
  "flight_status": "scheduled",
  "health_status": "healthy",
  "approval_status": "pending"
});
var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};
fetch("http://localhost:5000/api/flight/createFlight", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

# 根据航班ID获取详细信息

## **接口地址**

`/flight/getFlight/{flight_id}`

## **传入参数**

- 要求鉴权：是
- 请求方式：GET
- 传入方式：路径参数
- 要求权限：FLIGHT.READ

| **参数名**   | **描述** | **是否必须** | **类型** |
|-----------|--------|----------|--------|
| flight_id | 航班ID   | 是        | string |


## **返回值——成功**

```json
{
  "code": 0,
  "data": {
    "actual_arrival": "Sun, 27 Apr 2025 10:00:00 GMT",
    "actual_departure": "Fri, 25 Apr 2025 00:00:00 GMT",
    "aircraft_id": "AC002",
    "approval_status": "pending",
    "created_at": "Sun, 20 Apr 2025 18:09:09 GMT",
    "estimated_arrival": "Sun, 27 Apr 2025 10:00:00 GMT",
    "estimated_departure": "Fri, 25 Apr 2025 00:00:00 GMT",
    "flight_id": "9a29589d-f852-4675-89dc-d7282f3e5a45",
    "flight_status": "cancelled",
    "health_status": "healthy",
    "terminal_id": "244b6279-69d0-4397-b0d8-ef47ceda4e37",
    "updated_at": "Sun, 20 Apr 2025 18:09:09 GMT"
  },
  "msg": "添加航班成功"
}
```

## **返回值——未找到**

```json
{
  "code": 1,
  "data": {
    "error": "未找到ID为0f78d109-f1cd-4ffb-9099-5371960ea9eb的航班"
  },
  "msg": "航班未找到"
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
fetch("http://localhost:5000/api/flight/getFlight/0f78d109-f1cd-4ffb-9099-5371960ea9eb", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

# 更新航班

## **接口地址**

`/flight/updateFlight/{flight_id}`

## **传入参数**

- 要求鉴权：是
- 请求方式：POST
- 传入方式：json + 路径参数
- 要求权限：FLIGHT.UPDATE

| **参数名**             | **描述**     | **是否必须** | **类型**           |
|---------------------|------------|----------|------------------|
| flight_id           | 航班ID（路径参数） | 是        | string           |
| aircraft_id         | 飞机ID       | 否        | string           |
| terminal_id         | 航站楼ID      | 否        | string           |
| estimated_departure | 预计起飞时间     | 否        | datetime (ISO格式) |
| estimated_arrival   | 预计到达时间     | 否        | datetime (ISO格式) |
| flight_status       | 航班状态       | 否        | string           |
| actual_departure    | 实际起飞时间     | 否        | datetime (ISO格式) |
| actual_arrival      | 实际到达时间     | 否        | datetime (ISO格式) |
| health_status       | 健康状态       | 否        | string           |
| approval_status     | 审批状态       | 否        | string           |


## **返回值——成功**

```json
{
  "code": 0,
  "data": {
    "flight_id": "0f78d109-f1cd-4ffb-9099-5371960ea9eb",
    "aircraft_id": "aircraft123",
    "terminal_id": "terminal456",
    "estimated_departure": "2023-12-01T09:00:00",
    "estimated_arrival": "2023-12-01T11:00:00",
    "flight_status": "scheduled",
    "actual_departure": null,
    "actual_arrival": null,
    "health_status": "healthy",
    "approval_status": "approved",
    "created_at": "2023-11-30T12:00:00",
    "updated_at": "2023-11-30T12:30:00"
  },
  "msg": "更新航班成功"
}
```

## **返回值——未找到**

```json
{
  "code": 1,
  "data": {
    "error": "未找到ID为0f78d109-f1cd-4ffb-9099-5371960ea9eb的航班或更新失败"
  },
  "msg": "更新航班失败"
}
```

## **返回值——时间冲突**

```json
{
  "code": 1,
  "data": {
    "error": "同一飞机在该时间段内已被安排其他航班"
  },
  "msg": "时间冲突错误"
}
```

## **请求示例**

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTEyNzI1NCwianRpIjoiMjk4MTM3ZTUtZWRmOS00ZWYyLTlhY2EtNDllN2YwYTZhMjc5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU1Y2RlYWZkLTA5NmMtNDUzZC05MzM5LTU1ODY5MzE5MzJiYyIsIm5iZiI6MTc0NTEyNzI1NCwiY3NyZiI6IjU0NmEyMWI0LWYyY2QtNGQ3OC1iZGYxLWE5YmVmMWYyOGY0ZCIsImV4cCI6MTc0NTIxMzY1NH0.8fZIwcWjVk4fFL_hSVUibjZB1KkpSYN4-tHP8AWTYk4");
myHeaders.append("Content-Type", "application/json");
var raw = JSON.stringify({
  "estimated_departure": "2023-12-01T09:00:00",
  "estimated_arrival": "2023-12-01T11:00:00",
  "approval_status": "approved"
});
var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};
fetch("http://localhost:5000/api/flight/updateFlight/0f78d109-f1cd-4ffb-9099-5371960ea9eb", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

# 删除航班

## **接口地址**

`/flight/deleteFlight/{flight_id}`

## **传入参数**

- 要求鉴权：是
- 请求方式：DELETE
- 传入方式：路径参数
- 要求权限：FLIGHT.DELETE

| **参数名**   | **描述** | **是否必须** | **类型** |
|-----------|--------|----------|--------|
| flight_id | 航班ID   | 是        | string |


## **返回值——成功**

```json
{
  "code": 0,
  "data": null,
  "msg": "删除航班成功"
}
```

## **返回值——未找到**

```json
{
  "code": 1,
  "data": {
    "error": "未找到ID为0f78d109-f1cd-4ffb-9099-5371960ea9eb的航班或删除失败"
  },
  "msg": "删除航班失败"
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
fetch("http://localhost:5000/api/flight/deleteFlight/0f78d109-f1cd-4ffb-9099-5371960ea9eb", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

# 分页查询航班

## **接口地址**

`/flight/searchFlight`

## **传入参数**

- 要求鉴权：是
- 请求方式：GET
- 传入方式：query参数
- 要求权限：FLIGHT.READ

| **参数名**                   | **描述**      | **是否必须** | **类型**         |
|---------------------------|-------------|----------|----------------|
| aircraft_id               | 飞机ID        | 否        | string         |
| terminal_id               | 航站楼ID       | 否        | string         |
| flight_status             | 航班状态        | 否        | string         |
| health_status             | 健康状态        | 否        | string         |
| approval_status           | 审批状态        | 否        | string         |
| aircraft_name             | 飞机名称（模糊查询）  | 否        | string         |
| terminal_name             | 航站楼名称（模糊查询） | 否        | string         |
| estimated_departure_start | 预计起飞起始时间    | 否        | string (ISO格式) |
| estimated_departure_end   | 预计起飞结束时间    | 否        | string (ISO格式) |
| estimated_arrival_start   | 预计到达起始时间    | 否        | string (ISO格式) |
| estimated_arrival_end     | 预计到达结束时间    | 否        | string (ISO格式) |
| actual_departure_start    | 实际起飞起始时间    | 否        | string (ISO格式) |
| actual_departure_end      | 实际起飞结束时间    | 否        | string (ISO格式) |
| actual_arrival_start      | 实际到达起始时间    | 否        | string (ISO格式) |
| actual_arrival_end        | 实际到达结束时间    | 否        | string (ISO格式) |
| current_page              | 页码，默认值为1    | 否        | integer        |
| page_size                 | 每页数量，默认值为10 | 否        | integer        |


## **返回值——成功**

```json
{
    "code": 0,
    "data": {
        "data": [
            {
                "actual_arrival": "Sun, 27 Apr 2025 10:00:00 GMT",
                "actual_departure": "Fri, 25 Apr 2025 00:00:00 GMT",
                "aircraft_id": "AC002",
                "aircraft_name": "Sky Beta",
                "approval_status": "approved",
                "created_at": "Sun, 20 Apr 2025 18:07:55 GMT",
                "estimated_arrival": "Sun, 27 Apr 2025 10:00:00 GMT",
                "estimated_departure": "Fri, 25 Apr 2025 00:00:00 GMT",
                "flight_id": "9a29589d-f852-4675-89dc-d7282f3e5a45",
                "flight_status": "cancelled",
                "health_status": "healthy",
                "terminal_id": "244b6279-69d0-4397-b0d8-ef47ceda4e37",
                "terminal_name": "航站楼7",
                "updated_at": "Sun, 20 Apr 2025 18:07:55 GMT"
            },
            {
                "actual_arrival": "Sun, 27 Apr 2025 10:00:00 GMT",
                "actual_departure": "Fri, 25 Apr 2025 00:00:00 GMT",
                "aircraft_id": "AC007",
                "aircraft_name": "Thunder Eta",
                "approval_status": "pending",
                "created_at": "Sun, 20 Apr 2025 15:46:41 GMT",
                "estimated_arrival": "Sun, 27 Apr 2025 10:00:00 GMT",
                "estimated_departure": "Fri, 25 Apr 2025 00:00:00 GMT",
                "flight_id": "4ed86373-b98c-4419-8730-2e6ca1514bd2",
                "flight_status": "cancelled",
                "health_status": "healthy",
                "terminal_id": "244b6279-69d0-4397-b0d8-ef47ceda4e37",
                "terminal_name": "航站楼7",
                "updated_at": "Sun, 20 Apr 2025 15:46:41 GMT"
            },
            {
                "actual_arrival": "Mon, 21 Apr 2025 10:00:00 GMT",
                "actual_departure": "Sun, 20 Apr 2025 00:00:00 GMT",
                "aircraft_id": "AC007",
                "aircraft_name": "Thunder Eta",
                "approval_status": "pending",
                "created_at": "Sun, 20 Apr 2025 15:44:23 GMT",
                "estimated_arrival": "Mon, 21 Apr 2025 10:00:00 GMT",
                "estimated_departure": "Sun, 20 Apr 2025 00:00:00 GMT",
                "flight_id": "b2509550-c2c6-4de4-af82-1a09a6d5c30e",
                "flight_status": "scheduled",
                "health_status": "healthy",
                "terminal_id": "244b6279-69d0-4397-b0d8-ef47ceda4e37",
                "terminal_name": "航站楼7",
                "updated_at": "Sun, 20 Apr 2025 15:44:23 GMT"
            }
        ],
        "pagination": {
            "current_page": 1,
            "page_size": 10,
            "total": 3,
            "total_pages": 1
        }
    },
    "msg": "查询航班列表成功"
}
```

## **返回值——参数错误**

```json
{
  "code": 1,
  "data": {
    "error": "页码和每页大小必须大于0"
  },
  "msg": "航班数据无效"
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
fetch("http://localhost:5000/api/flight/searchFlight?aircraft_name=Boeing&estimated_departure_start=2023-12-01T00:00:00&estimated_departure_end=2023-12-02T00:00:00&current_page=1&page_size=10", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```