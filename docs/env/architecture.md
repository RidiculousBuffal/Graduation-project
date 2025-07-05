---
next:
  text: Apifox调试
  link: /docs/env/apifox
prev:
    text: 开始
    link: /docs/env/index
---

# 项目结构

## 后端

### 1. 核心框架

本项目后端采用**Flask**作为主要Web框架。Flask是一个轻量级的Python
Web框架，提供了灵活性和可扩展性，非常适合构建API和Web服务。项目利用Flask的模块化特性，实现了清晰的代码组织结构和路由管理。

### 2. 数据访问层

#### 2.1 数据库与ORM

- **SQLAlchemy**：项目通过Flask-SQLAlchemy扩展集成了SQLAlchemy ORM框架，实现了对象关系映射
- **数据映射模式**：采用Mapper设计模式（如`aircraftMapper.py`, `flightMapper.py`等）处理数据转换，有效分离了数据访问逻辑和业务逻辑

#### 2.2 数据库迁移

- **Alembic**：用于数据库版本控制和迁移管理，确保数据库结构与应用模型同步

### 3. 异步任务处理

- **Celery**：实现了异步任务队列，用于处理耗时操作，提高系统响应性能
- 结合定时任务功能，能够按计划执行周期性任务

### 4. 数据验证与模型定义

- **Pydantic**：用于数据验证、序列化和反序列化
- 提供类型安全的数据模型，确保API接收和返回的数据符合预期格式

### 5. 高级数据存储

#### 5.1 向量数据库

- **Weaviate**：项目集成了Weaviate向量数据库，用于处理向量搜索和语义查询
- 支持复杂的相似度搜索功能

#### 5.2 缓存层

- **Redis**：用作缓存系统和消息队列，与Celery协同工作提升系统性能

### 6. 图像处理与机器学习

- **OpenCV**：提供强大的图像处理功能
- **面部识别模块**：实现了基于OpenCV的面部识别功能
- **科学计算支持**：集成NumPy和SciPy等库，用于数据处理和分析

### 7. 系统功能模块

#### 7.1 权限管理

- 基于角色的访问控制系统（RBAC）
- 精细化的权限分配机制

#### 7.2 审计日志

- 完整的操作审计跟踪功能
- 记录关键系统操作，支持合规性要求

#### 7.3 业务领域模块

- **航班管理**：处理航班信息、调度和状态跟踪
- **飞机管理**：包括飞机信息、类型管理和参考图像
- **检查记录**：飞机检查流程和记录管理

### 8. 开发与测试支持

- **pytest**：单元测试和集成测试框架
- **coverage**：代码覆盖率分析工具，确保测试的完整性

## 前端

### 前端框架层

``` 
React 19.1.0
├── React DOM 19.1.0
├── TypeScript 5.8.3
└── @ant-design/v5-patch-for-react-19 1.0.3
```

### 构建工具链

``` 
Vite 6.3.5
├── @vitejs/plugin-react 4.4.1
├── ESLint 9.25.0
├── TypeScript ESLint 8.30.1
└── Terser 5.43.1
```

### UI组件库

``` 
Ant Design 5.25.4
├── @lobehub/ui 2.5.6
├── Lucide React 0.513.0
└── react-nice-avatar 1.5.0
```

### 状态管理

``` 
Zustand 5.0.5
└── Immer 10.1.1
```

### 路由管理

``` 
React Router 7.6.2
```

### 3D渲染引擎

``` 
Three.js 0.177.0
├── @react-three/fiber 9.1.2
└── @react-three/drei 10.1.2
```

### 数据处理

``` 
Zod 3.25.56
├── Validator 13.15.15
├── QS 6.14.0
└── @uiw/react-json-view 2.0.0-alpha.32
```

### 项目架构说明

#### 目录结构

``` 
src/
├── api/           # API接口层
├── components/    # 公共组件
├── pages/         # 页面组件
├── store/         # 状态管理
├── services/      # 业务服务
├── utils/         # 工具函数
├── assets/        # 静态资源
├── consts/        # 常量配置
└── publicTypes/   # 公共类型定义
```

## 发版/开发流程

<ThemeImage
lightSrc="/architecture-light.png"
darkSrc="/architecture-dark.png"
alt="开发流程"
/>