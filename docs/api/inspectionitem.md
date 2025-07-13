# 新增检测条目
## 请求方式  
```bash
  POST /inspection_item/create
```
- 权限  `INSPECTION_ITEM_ADD`
- 请求 Header   `Authorization`
- 请求参数（JSON Body 对应 DTO：InspectionItemCreateDTO）
  ```json
  {
    "item_name": "机体裂纹检测",                
    "inspection_id": "insp_123456",            
    "description": "机身左翼根部裂纹检测",        
    "model_id": "model_yolo_v8_defect",        
    "item_point": {                             
      "point": {
        "x": 0.1, "y": 0.2, "w": 0.3, "h": 0.4    
      },
      "fileInfo": {
        "download_url": "...", 
        "filename": "ref.png",
        "ipfs_cid": "...",
        "mime_type": "image/png",
        "size": 12345
      }
    },
    "result": []                               
  }
  ```
## 响应 
  ```json
  {
    "item_id": "item_abcdef",                  
    "item_name": "机体裂纹检测",
    "inspection_id": "insp_123456",
    "description": "机身左翼根部裂纹检测",
    "model_id": "model_yolo_v8_defect",
    "model_name": "YoloV8 裂纹检测模型",        
    "model_description": "...",
    "item_point": {  },
    "result": [], 
    "created_at": "2024-06-01T12:00:00Z",
    "updated_at": "2024-06-01T12:00:00Z"
  }
  ```

# 根据 ID 获取检测条目详情

## 请求方式
```bash
  GET /inspection_item/{item_id}
```
- 权限  `INSPECTION_ITEM_READ`
- 请求参数:   Path 参数：`item_id`
## 响应
```json
  {
    "item_id": "item_abcdef",                  
    "item_name": "机体裂纹检测",
    "inspection_id": "insp_123456",
    "description": "机身左翼根部裂纹检测",
    "model_id": "model_yolo_v8_defect",
    "model_name": "YoloV8 裂纹检测模型",        
    "model_description": "...",
    "item_point": {  },
    "result": [], 
    "created_at": "2024-06-01T12:00:00Z",
    "updated_at": "2024-06-01T12:00:00Z"
  }
  ```

# 更新检测条目
## 请求方式
```bash
PUT /inspection_item/{item_id}
```
- 权限  
  `INSPECTION_ITEM_UPDATE`
- 请求 Body 对应 DTO：`InspectionItemUpdateDTO`
  ```json
  {
    "item_name": "机体裂纹检测-更新名称",  
    "description": "更新描述",             
    "model_id": "model_new",             
    "item_point": {  },               
    "result": [                         
      {
        "inputImage": {  },
        "resultImage": {
          "boxes": [
            {"label":"crack","confidence":0.93,"points":{"x1":10,"y1":20,"x2":110,"y2":120}}
          ],
          "resultImage": {  }
        },
        "isPassed": false,
        "progress": "done",
        "version": 1
      }
    ]
  }
  ```


# 删除检测条目
## 请求方式
```bash
  DELETE /inspection_item/{item_id}
```
- 权限 `INSPECTION_ITEM_DELETE`
## 响应
    - 成功：`{"code":0,"msg":"删除成功","data":true}`
    - 不存在返回 404

# 分页查询检测条目列表
## 请求方式
```bash
GET /inspection_item/list
```
- 权限 `INSPECTION_ITEM_READ`
- 查询参数（Query）
    - inspection_id (string, 必填)
    - current_page (int, 默认 1)
    - page_size (int, 默认 10)
## 响应 data（InspectionItemPagedResponseDTO）
  ```json
  {
    "data": [ ],    
    "pagination": {                  
      "current_page": 1,
      "page_size": 10,
      "total": 35,
      "total_pages": 4
    }
  }
  ```

