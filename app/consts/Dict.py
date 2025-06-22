class DictionaryData:
    # 状态分类（父项）
    STATUS = {
        "dict_key": "status",
        "dict_name": "状态类",
        "description": "所有状态类字典的总分类",
        "parent_key": None,
        "sort_order": 1
    }
    # 飞行状态
    FLIGHT_STATUS = {
        "dict_key": "flight_status",
        "dict_name": "飞行状态",
        "description": "飞机飞行流程状态",
        "parent_key": "status",
        "sort_order": 10
    }
    SCHEDULED = {
        "dict_key": "scheduled",
        "dict_name": "已排班",
        "description": "航班已安排",
        "parent_key": "flight_status",
        "sort_order": 11
    }
    BOARDING = {
        "dict_key": "boarding",
        "dict_name": "登机中",
        "description": "开始登机",
        "parent_key": "flight_status",
        "sort_order": 12
    }
    DEPARTED = {
        "dict_key": "departed",
        "dict_name": "已起飞",
        "description": "飞机已起飞",
        "parent_key": "flight_status",
        "sort_order": 13
    }
    ARRIVED = {
        "dict_key": "arrived",
        "dict_name": "已到达",
        "description": "航班已到达目的地",
        "parent_key": "flight_status",
        "sort_order": 14
    }
    DELAYED = {
        "dict_key": "delayed",
        "dict_name": "延误",
        "description": "航班延误",
        "parent_key": "flight_status",
        "sort_order": 15
    }
    CANCELLED = {
        "dict_key": "cancelled",
        "dict_name": "已取消",
        "description": "航班取消",
        "parent_key": "flight_status",
        "sort_order": 16
    }
    # 健康状态
    HEALTH_STATUS = {
        "dict_key": "health_status",
        "dict_name": "健康状态",
        "description": "飞机健康状态",
        "parent_key": "status",
        "sort_order": 20
    }
    HEALTHY = {
        "dict_key": "healthy",
        "dict_name": "健康",
        "description": "飞机处于健康状态",
        "parent_key": "health_status",
        "sort_order": 21
    }
    MAINTENANCE = {
        "dict_key": "maintenance",
        "dict_name": "维护中",
        "description": "飞机需要维护",
        "parent_key": "health_status",
        "sort_order": 22
    }
    FAULT = {
        "dict_key": "fault",
        "dict_name": "故障",
        "description": "飞机出现故障",
        "parent_key": "health_status",
        "sort_order": 23
    }
    # 审批状态
    APPROVAL_STATUS = {
        "dict_key": "approval_status",
        "dict_name": "审批状态",
        "description": "飞行审批进度",
        "parent_key": "status",
        "sort_order": 30
    }
    PENDING = {
        "dict_key": "pending",
        "dict_name": "待审批",
        "description": "待审批",
        "parent_key": "approval_status",
        "sort_order": 31
    }
    APPROVED = {
        "dict_key": "approved",
        "dict_name": "已通过",
        "description": "审批通过",
        "parent_key": "approval_status",
        "sort_order": 32
    }
    REJECTED = {
        "dict_key": "rejected",
        "dict_name": "已拒绝",
        "description": "审批拒绝",
        "parent_key": "approval_status",
        "sort_order": 33
    }
    # 任务状态
    TASK_STATUS = {
        "dict_key": "task_status",
        "dict_name": "任务状态",
        "description": "维护任务状态",
        "parent_key": "status",
        "sort_order": 40
    }
    TASK_PENDING = {
        "dict_key": "task_pending",
        "dict_name": "待处理",
        "description": "任务未开始",
        "parent_key": "task_status",
        "sort_order": 41
    }
    TASK_IN_PROGRESS = {
        "dict_key": "task_in_progress",
        "dict_name": "进行中",
        "description": "任务正在执行",
        "parent_key": "task_status",
        "sort_order": 42
    }
    TASK_PAUSED = {
        "dict_key": "task_paused",
        "dict_name": "暂停",
        "description": "任务因故暂停",
        "parent_key": "task_status",
        "sort_order": 43
    }
    TASK_COMPLETED = {
        "dict_key": "task_completed",
        "dict_name": "已完成",
        "description": "任务完全结束",
        "parent_key": "task_status",
        "sort_order": 44
    }
    TASK_FAILED = {
        "dict_key": "task_failed",
        "dict_name": "失败",
        "description": "任务失败",
        "parent_key": "task_status",
        "sort_order": 45
    }
    # 检查状态
    INSPECTION_STATUS = {
        "dict_key": "inspection_status",
        "dict_name": "检查状态",
        "description": "检查/巡检记录状态",
        "parent_key": "status",
        "sort_order": 50
    }
    INSPECTION_NOT_STARTED = {
        "dict_key": "inspection_not_started",
        "dict_name": "未开始",
        "description": "还未开始检查",
        "parent_key": "inspection_status",
        "sort_order": 51
    }
    INSPECTION_IN_PROGRESS = {
        "dict_key": "inspection_in_progress",
        "dict_name": "进行中",
        "description": "正在检查",
        "parent_key": "inspection_status",
        "sort_order": 52
    }
    INSPECTION_PASSED = {
        "dict_key": "inspection_passed",
        "dict_name": "已通过",
        "description": "检查通过",
        "parent_key": "inspection_status",
        "sort_order": 53
    }
    INSPECTION_FAILED = {
        "dict_key": "inspection_failed",
        "dict_name": "未通过",
        "description": "检查未通过",
        "parent_key": "inspection_status",
        "sort_order": 54
    }
    PENDING_CHECK = {
        "dict_key": "pending_check",
        "dict_name": "等待检查",
        "description": "还没开始健康检查",
        "parent_key": "health_status",
        "sort_order": 55
    }
