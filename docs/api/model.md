# 模型

# 获取所有检测模型

```bash
GET /getmodels
```

- 权限  
  需登录（`jwt_required`）
- 请求参数

# 响应 data（ModelDTO 数组）

  ```json
  [
  {
    "model_id": "model_yolo_v8_defect",
    "model_name": "YoloV8 裂纹检测模型",
    "model_description": "专用于机身裂纹检测",
    "model_api_path": "/models/yolov8/defect"
  },
  {
    "model_id": "model_yolo_v8_bolthead",
    "model_name": "螺栓头检测",
    "model_description": "...",
    "model_api_path": "/models/yolov8/bolt"
  }
]
  ```
