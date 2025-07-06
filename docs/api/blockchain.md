# 区块链状态查询

## 接口地址

```bash
/blockChainStatus
```

## 传入参数

• 要求鉴权：否

• 请求方式：GET

• 传入方式：QueryString

• 要求权限：无

| **参数名** | **描述** | **是否必须** | **类型** |
|---------|--------|----------|--------|
| 无       | 无需传入参数 | -        | -      |

## 返回值——成功

```json
{
  "code": 0,
  "data": {
    "abi": [],
    "address": "0x123...abc",
    "url": "http://blockchain-rpc-url",
    "status": "connected"
  },
  "msg": "success"
}
```

## 请求示例

```JavaScript
fetch("http://localhost:5000/api/blockChainStatus")
    .then(response => response.json())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```

---

# 审计日志分页查询

## 接口地址

`/searchAuditLog`

## 传入参数

• 要求鉴权：是（JWT）

• 请求方式：GET

• 传入方式：QueryString

• 要求权限：需要 LOG_READ 权限

| **参数名**      | **描述** | **是否必须** | **类型** |
|--------------|--------|----------|--------|
| current_page | 当前页码   | 否        | int    |
| page_size    | 每页条数   | 否        | int    |

## 返回值——成功

```json
{
  "code": 0,
  "data": {
    "data": [
      {
        "log_id": 1,
        "user_id": "user123",
        "action": {
          "userId": "user123",
          "event_name": "update_part",
          "input_parameter": {},
          "result": {}
        },
        "timestamp": "2024-06-06T12:34:56.123456",
        "blockchain_tx_hash": "0xabc...",
        "blockchain_block_number": 123456,
        "blockchain_operator": "0x987..."
      }
    ],
    "pagination": {
      "current_page": 1,
      "page_size": 10,
      "total": 25,
      "total_pages": 3
    }
  },
  "msg": "success"
}
```

## 返回值——权限不足

```json
{
  "code": 403,
  "data": null,
  "msg": "权限不足"
}
```

## 请求示例

```JavaScript
var myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer your_jwt_token");
fetch("http://localhost:5000/api/searchAuditLog?current_page=1&page_size=10", {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
})
    .then(response => response.json())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```