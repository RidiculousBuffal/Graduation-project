from datetime import datetime
from typing import Optional

from sqlalchemy import select, between
from sqlalchemy.orm import joinedload

from app.DTO.pagination import PaginationDTO
from app.DTO.tasks import TaskCreateDTO, TaskUpdateDTO, TaskDTO, TaskDetailDTO, TaskPagedResponseDTO
from app.ext.extensions import db
from app.models.aircraft import Aircraft
from app.models.auth import User
from app.models.flight import Flight
from app.models.task import Task


class TaskMapper:
    @staticmethod
    def create(task_data: TaskCreateDTO) -> TaskDTO:
        """创建任务记录"""
        task = Task(
            flight_id=task_data.flight_id,
            estimated_start=task_data.estimated_start,
            estimated_end=task_data.estimated_end,
            admin_id=task_data.admin_id,
            task_status=task_data.task_status
        )
        db.session.add(task)
        db.session.commit()
        return TaskDTO.model_validate(task.to_dict())

    @staticmethod
    def get_by_id(task_id: str) -> Optional[TaskDetailDTO]:
        """根据ID查询任务记录，包含详细信息"""
        task = (db.session.query(Task)
                .options(
            joinedload(Task.status_dict),
        )
                .get(task_id))

        if not task:
            return None

        # 获取关联的航班和飞机信息
        flight = db.session.get(Flight, task.flight_id)
        aircraft = None
        if flight and flight.aircraft_id:
            aircraft = db.session.get(Aircraft, flight.aircraft_id)

        # 获取管理员信息
        admin = None
        if task.admin_id:
            admin = db.session.get(User, task.admin_id)

        return TaskDetailDTO(
            task_id=task.task_id,
            flight_id=task.flight_id,
            flight_number=flight.flight_number if flight and hasattr(flight, 'flight_number') else None,
            aircraft_id=flight.aircraft_id if flight else None,
            aircraft_name=aircraft.aircraft_name if aircraft else None,
            estimated_start=task.estimated_start,
            estimated_end=task.estimated_end,
            actual_start=task.actual_start,
            actual_end=task.actual_end,
            admin_id=task.admin_id,
            admin_name=admin.name if admin else None,
            task_status=task.task_status,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    @staticmethod
    def update(task_id: str, update_data: TaskUpdateDTO) -> Optional[TaskDTO]:
        """更新任务记录"""
        task = db.session.get(Task, task_id)
        if not task:
            return None

        if update_data.flight_id is not None:
            task.flight_id = update_data.flight_id
        if update_data.estimated_start is not None:
            task.estimated_start = update_data.estimated_start
        if update_data.estimated_end is not None:
            task.estimated_end = update_data.estimated_end
        if update_data.actual_start is not None:
            task.actual_start = update_data.actual_start
        if update_data.actual_end is not None:
            task.actual_end = update_data.actual_end
        if update_data.admin_id is not None:
            task.admin_id = update_data.admin_id
        if update_data.task_status is not None:
            task.task_status = update_data.task_status

        db.session.commit()
        return TaskDTO.model_validate(task.to_dict())

    @staticmethod
    def delete(task_id: str) -> bool:
        """删除任务记录"""
        task = db.session.get(Task, task_id)
        if not task:
            return False
        db.session.delete(task)
        db.session.commit()
        return True

    @staticmethod
    def search(
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
        """分页查询任务记录"""
        query = select(Task).options(joinedload(Task.status_dict))

        # 基本查询条件
        if flight_id:
            query = query.where(Task.flight_id == flight_id)
        if admin_id:
            query = query.where(Task.admin_id == admin_id)
        if task_status:
            query = query.where(Task.task_status == task_status)

        # 关联Flight和Aircraft表查询
        if aircraft_id or aircraft_name:
            query = query.join(Flight)
            if aircraft_id:
                query = query.where(Flight.aircraft_id == aircraft_id)
            if aircraft_name:
                query = query.join(Aircraft)
                query = query.where(Aircraft.aircraft_name.ilike(f"%{aircraft_name}%"))

        # 关联User表查询管理员名称
        if admin_name:
            query = query.join(User, Task.admin_id == User.user_id)
            query = query.where(User.name.ilike(f"%{admin_name}%"))

        # 时间范围查询
        if estimated_start_from and estimated_start_to:
            query = query.where(between(Task.estimated_start, estimated_start_from, estimated_start_to))
        elif estimated_start_from:
            query = query.where(Task.estimated_start >= estimated_start_from)
        elif estimated_start_to:
            query = query.where(Task.estimated_start <= estimated_start_to)

        if estimated_end_from and estimated_end_to:
            query = query.where(between(Task.estimated_end, estimated_end_from, estimated_end_to))
        elif estimated_end_from:
            query = query.where(Task.estimated_end >= estimated_end_from)
        elif estimated_end_to:
            query = query.where(Task.estimated_end <= estimated_end_to)

        # 排序和分页
        query = query.order_by(Task.created_at.desc())
        pagination = db.paginate(
            select=query,
            page=page_num,
            per_page=page_size,
            max_per_page=100,
            error_out=False,
            count=True
        )

        tasks_data = []
        for task in pagination.items:
            # 获取关联的航班和飞机信息
            flight = db.session.get(Flight, task.flight_id)
            aircraft = None
            if flight and hasattr(flight, 'aircraft_id') and flight.aircraft_id:
                aircraft = db.session.get(Aircraft, flight.aircraft_id)

            # 获取管理员信息
            admin = None
            if task.admin_id:
                admin = db.session.get(User, task.admin_id)

            tasks_data.append(TaskDetailDTO(
                task_id=task.task_id,
                flight_id=task.flight_id,
                flight_number=flight.flight_number if flight and hasattr(flight, 'flight_number') else None,
                aircraft_id=flight.aircraft_id if flight and hasattr(flight, 'aircraft_id') else None,
                aircraft_name=aircraft.aircraft_name if aircraft else None,
                estimated_start=task.estimated_start,
                estimated_end=task.estimated_end,
                actual_start=task.actual_start,
                actual_end=task.actual_end,
                admin_id=task.admin_id,
                admin_name=admin.name if admin else None,
                task_status=task.task_status,
                created_at=task.created_at,
                updated_at=task.updated_at
            ))

        pagination_dto = PaginationDTO(
            current_page=pagination.page,
            page_size=pagination.per_page,
            total=pagination.total or 0,
            total_pages=pagination.pages
        )

        response = TaskPagedResponseDTO(
            data=tasks_data,
            pagination=pagination_dto
        )
        return response
