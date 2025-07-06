# **创建任务**

## **接口地址**

```bash
POST /task/create
```

## **鉴权/权限**

- 要求鉴权：是（JWT）
- 要求权限：TASK_ADD

## **请求方式**

POST（application/json）

## **参数**

| **参数名**         | **描述**           | **是否必须** | **类型**           |
|-----------------|------------------|----------|------------------|
| flight_id       | 航班ID             | 是        | string           |
| estimated_start | 预计开始时间           | 否        | string (ISO8601) |
| estimated_end   | 预计结束时间           | 否        | string (ISO8601) |
| admin_id        | 管理员ID（自动传入，无需上传） | 否        | string           |
| task_status     | 任务状态             | 否        | string           |

## **成功返回示例**

```json
{
  "code": 0,
  "data": {
    "task_id": "xxx",
    "flight_id": "xxx",
    "estimated_start": "2024-06-20T12:30:00",
    "estimated_end": "2024-06-20T13:00:00",
    "actual_start": null,
    "actual_end": null,
    "admin_id": "admin-xxx",
    "task_status": "pending",
    "created_at": "2024-06-20T11:01:00",
    "updated_at": "2024-06-20T11:01:00"
  },
  "msg": "任务创建成功"
}
```

## **失败返回示例**

# **获取任务详情**

## **接口地址**

`GET /task/getTaskById/<task_id>`

## **鉴权/权限**

- 要求鉴权：是（JWT）
- 要求权限：TASK_READ

## **请求参数**

- task_id（在URL路径中）

## **成功返回示例**

```json
{
  "code": 0,
  "data": {
    "task_id": "xxx",
    "flight_id": "xxx",
    "aircraft_id": "xxx",
    "aircraft_name": "xxx",
    "estimated_start": "2024-06-20T12:30:00",
    "estimated_end": "2024-06-20T13:00:00",
    "actual_start": null,
    "actual_end": null,
    "admin_id": "xxx",
    "admin_name": "管理员A",
    "task_status": "pending",
    "created_at": "2024-06-20T11:01:00",
    "updated_at": "2024-06-20T11:01:00"
  },
  "msg": "任务查询成功"
}
```

# **更新任务**

## **接口地址**

`PUT /api/task/updateTask/<task_id>`

## **鉴权/权限**

- 要求鉴权：是（JWT）
- 要求权限：TASK_UPDATE

## **请求体（JSON）参数**

| **参数名**         | **描述** | **是否必须** | **类型**          |
|-----------------|--------|----------|-----------------|
| flight_id       | 航班ID   | 否        | string          |
| estimated_start | 预计开始   | 否        | string(ISO8601) |
| estimated_end   | 预计结束   | 否        | string(ISO8601) |
| actual_start    | 实际开始   | 否        | string(ISO8601) |
| actual_end      | 实际结束   | 否        | string(ISO8601) |
| admin_id        | 管理员ID  | 否        | string          |
| task_status     | 任务状态   | 否        | string          |

## **返回示例**

（成功与上方创建一致，仅 msg 不同；失败 msg 异常/未找到均出错）

# **删除任务**

**接口地址**

`DELETE /api/task/deleteTask/<task_id>`

## **鉴权/权限**

- 要求鉴权：是（JWT）
- 要求权限：TASK_DELETE

## **请求参数**

- task_id（URL路径）

## **成功返回示例**

```json
{
  "code": 0,
  "data": true,
  "msg": "任务删除成功"
}
```

# **分页&条件查询任务**

## **接口地址**

`GET /api/task/search`

## **鉴权/权限**

- 要求鉴权：是（JWT）
- 要求权限：TASK_READ

## **查询参数**

（全部为URL参数，均为可选，分页参数必须）

| **参数名**              | **描述** | **类型**          |
|----------------------|--------|-----------------|
| flight_id            | 航班ID   | string          |
| admin_id             | 管理员ID  | string          |
| task_status          | 任务状态   | string          |
| aircraft_id          | 飞机ID   | string          |
| aircraft_name        | 飞机名称   | string          |
| admin_name           | 管理员姓名  | string          |
| estimated_start_from | 预计开始起  | string(ISO8601) |
| estimated_start_to   | 预计开始止  | string(ISO8601) |
| estimated_end_from   | 预计结束起  | string(ISO8601) |
| estimated_end_to     | 预计结束止  | string(ISO8601) |
| actual_start_from    | 实际开始起  | string(ISO8601) |
| actual_start_to      | 实际开始止  | string(ISO8601) |
| actual_end_from      | 实际结束起  | string(ISO8601) |
| actual_end_to        | 实际结束止  | string(ISO8601) |
| current_page（必须）     | 页码     | int             |
| page_size（必须）        | 每页个数   | int             |

**返回值**

```json
{
  "code": 0,
  "data": {
    "data": [
      {
        "task_id": "xxx",
        "flight_id": "xxx",
        "aircraft_id": "xxx",
        "aircraft_name": "xxx",
        "...": "..."
      }
    ],
    "pagination": {
      "current_page": 1,
      "page_size": 10,
      "total": 100,
      "total_pages": 10
    }
  },
  "msg": "任务查询成功"
}
```

# **创建检查记录**

## **接口地址**

`POST /inspection/create`

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