from datetime import datetime
from typing import Optional

from app.DTO.tasks import TaskCreateDTO, TaskUpdateDTO, TaskDTO, TaskDetailDTO, TaskPagedResponseDTO
from app.mapper.tasks.taskMapper import TaskMapper


class TaskService:
    """任务服务类"""

    @staticmethod
    def create_task(task_data: TaskCreateDTO) -> TaskDTO:
        """
        创建新的任务
        :param task_data: 任务创建数据
        :return: 创建的任务信息
        """
        return TaskMapper.create(task_data)
    
    @staticmethod
    def get_task(task_id: str) -> Optional[TaskDetailDTO]:
        """
        根据ID获取任务详情
        :param task_id: 任务ID
        :return: 任务详情或None（如果不存在）
        """
        return TaskMapper.get_by_id(task_id)
    
    @staticmethod
    def update_task(task_id: str, update_data: TaskUpdateDTO) -> Optional[TaskDTO]:
        """
        更新任务信息
        :param task_id: 任务ID
        :param update_data: 更新的数据
        :return: 更新后的任务或None（如果任务不存在）
        """
        return TaskMapper.update(task_id, update_data)
    
    @staticmethod
    def delete_task(task_id: str) -> bool:
        """
        删除任务
        :param task_id: 任务ID
        :return: 删除操作是否成功
        """
        return TaskMapper.delete(task_id)
    
    @staticmethod
    def search_tasks(
            flight_id: Optional[str] = None,
            admin_id: Optional[str] = None,
            task_status: Optional[str] = None,
            aircraft_id: Optional[str] = None,
            aircraft_name: Optional[str] = None,
            admin_name: Optional[str] = None,
            estimated_start_from: Optional[datetime] = None,
            estimated_start_to: Optional[datetime] = None,
            estimated_end_from: Optional[datetime] = None,
            estimated_end_to: Optional[datetime] = None,
            page_num: int = 1,
            page_size: int = 10
    ) -> TaskPagedResponseDTO:
        """
        分页搜索任务
        :param flight_id: 航班ID
        :param admin_id: 管理员ID
        :param task_status: 任务状态
        :param aircraft_id: 飞机ID
        :param aircraft_name: 飞机名称
        :param admin_name: 管理员姓名
        :param estimated_start_from: 预计开始时间起点
        :param estimated_start_to: 预计开始时间终点
        :param estimated_end_from: 预计结束时间起点
        :param estimated_end_to: 预计结束时间终点
        :param page_num: 页码
        :param page_size: 每页大小
        :return: 分页后的任务列表
        """
        return TaskMapper.search(
            flight_id=flight_id,
            admin_id=admin_id,
            task_status=task_status,
            aircraft_id=aircraft_id,
            aircraft_name=aircraft_name,
            admin_name=admin_name,
            estimated_start_from=estimated_start_from,
            estimated_start_to=estimated_start_to,
            estimated_end_from=estimated_end_from,
            estimated_end_to=estimated_end_to,
            page_num=page_num,
            page_size=page_size
        )
