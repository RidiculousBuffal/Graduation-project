from datetime import datetime
from typing import Optional

from sqlalchemy import select, between
from sqlalchemy.orm import joinedload

from app.DTO.inspections import (
    InspectionRecordCreateDTO, InspectionRecordUpdateDTO,
    InspectionRecordDTO, InspectionRecordDetailDTO, InspectionRecordPagedResponseDTO
)
from app.DTO.pagination import PaginationDTO
from app.ext.extensions import db
from app.models.aircraft import Aircraft
from app.models.auth import User
from app.models.flight import Flight
from app.models.inspection import InspectionRecord
from app.models.task import Task


class InspectionRecordMapper:
    @staticmethod
    def create(inspection_data: InspectionRecordCreateDTO) -> InspectionRecordDTO:
        """创建检查记录"""
        inspection = InspectionRecord(
            inspection_name=inspection_data.inspection_name,
            task_id=inspection_data.task_id,
            executor_id=inspection_data.executor_id,
            reference_image_id=inspection_data.reference_image_id,
            progress=inspection_data.progress,
            start_time=inspection_data.start_time,
            end_time=inspection_data.end_time,
            inspection_status=inspection_data.inspection_status
        )
        db.session.add(inspection)
        db.session.commit()
        return InspectionRecordDTO.model_validate(inspection.to_dict())

    @staticmethod
    def get_by_id(inspection_id: str) -> Optional[InspectionRecordDetailDTO]:
        """根据ID查询检查记录，包含详细信息"""
        inspection = (db.session.query(InspectionRecord)
                      .options(
            joinedload(InspectionRecord.status_dict),
            joinedload(InspectionRecord.reference_image),
            joinedload(InspectionRecord.task)
        )
                      .get(inspection_id))

        if not inspection:
            return None

        # 获取执行工程师信息
        executor = None
        if inspection.executor_id:
            executor = db.session.get(User, inspection.executor_id)

        # 获取关联的任务、航班和飞机信息
        task = inspection.task
        flight = None
        aircraft = None

        if task:
            flight = db.session.get(Flight, task.flight_id)
            if flight and hasattr(flight, 'aircraft_id') and flight.aircraft_id:
                aircraft = db.session.get(Aircraft, flight.aircraft_id)

        return InspectionRecordDetailDTO(
            inspection_id=inspection.inspection_id,
            inspection_name=inspection.inspection_name,
            task_id=inspection.task_id,
            executor_id=inspection.executor_id,
            executor_name=executor.name if executor else None,
            reference_image_id=inspection.reference_image_id,
            reference_image_name=inspection.reference_image.image_name if inspection.reference_image else None,
            progress=inspection.progress,
            start_time=inspection.start_time,
            end_time=inspection.end_time,
            inspection_status=inspection.inspection_status,
            status_name=inspection.status_dict.dict_key,
            flight_id=flight.flight_id if flight else None,
            aircraft_id=flight.aircraft_id if flight and hasattr(flight, 'aircraft_id') else None,
            aircraft_name=aircraft.aircraft_name if aircraft else None,
            created_at=inspection.created_at,
            updated_at=inspection.updated_at
        )

    @staticmethod
    def update(inspection_id: str, update_data: InspectionRecordUpdateDTO) -> Optional[InspectionRecordDTO]:
        """更新检查记录"""
        inspection = db.session.get(InspectionRecord, inspection_id)
        if not inspection:
            return None

        if update_data.inspection_name is not None:
            inspection.inspection_name = update_data.inspection_name
        if update_data.task_id is not None:
            inspection.task_id = update_data.task_id
        if update_data.executor_id is not None:
            inspection.executor_id = update_data.executor_id
        if update_data.reference_image_id is not None:
            inspection.reference_image_id = update_data.reference_image_id
        if update_data.progress is not None:
            inspection.progress = update_data.progress
        if update_data.start_time is not None:
            inspection.start_time = update_data.start_time
        if update_data.end_time is not None:
            inspection.end_time = update_data.end_time
        if update_data.inspection_status is not None:
            inspection.inspection_status = update_data.inspection_status

        db.session.commit()
        return InspectionRecordDTO.model_validate(inspection.to_dict())

    @staticmethod
    def delete(inspection_id: str) -> bool:
        """删除检查记录"""
        inspection = db.session.get(InspectionRecord, inspection_id)
        if not inspection:
            return False
        db.session.delete(inspection)
        db.session.commit()
        return True

    @staticmethod
    def search(
            task_id: Optional[str] = None,
            executor_id: Optional[str] = None,
            inspection_status: Optional[str] = None,
            reference_image_id: Optional[str] = None,
            flight_id: Optional[str] = None,
            aircraft_id: Optional[str] = None,
            executor_name: Optional[str] = None,
            start_time_from: Optional[datetime] = None,
            start_time_to: Optional[datetime] = None,
            end_time_from: Optional[datetime] = None,
            end_time_to: Optional[datetime] = None,
            page_num: int = 1,
            page_size: int = 10
    ) -> InspectionRecordPagedResponseDTO:
        """分页查询检查记录"""
        query = select(InspectionRecord).options(
            joinedload(InspectionRecord.status_dict),
            joinedload(InspectionRecord.reference_image),
            joinedload(InspectionRecord.task)
        )

        # 基本查询条件
        if task_id:
            query = query.where(InspectionRecord.task_id == task_id)
        if executor_id:
            query = query.where(InspectionRecord.executor_id == executor_id)
        if inspection_status:
            query = query.where(InspectionRecord.inspection_status == inspection_status)
        if reference_image_id:
            query = query.where(InspectionRecord.reference_image_id == reference_image_id)

        # 关联Task和Flight表查询
        if flight_id:
            query = query.join(Task)
            query = query.where(Task.flight_id == flight_id)

        # 关联Flight和Aircraft表查询
        if aircraft_id:
            query = query.join(Task)
            query = query.join(Flight)
            query = query.where(Flight.aircraft_id == aircraft_id)

        # 关联User表查询执行工程师名称
        if executor_name:
            query = query.join(User, InspectionRecord.executor_id == User.user_id)
            query = query.where(User.name.ilike(f"%{executor_name}%"))

        # 时间范围查询
        if start_time_from and start_time_to:
            query = query.where(between(InspectionRecord.start_time, start_time_from, start_time_to))
        elif start_time_from:
            query = query.where(InspectionRecord.start_time >= start_time_from)
        elif start_time_to:
            query = query.where(InspectionRecord.start_time <= start_time_to)

        if end_time_from and end_time_to:
            query = query.where(between(InspectionRecord.end_time, end_time_from, end_time_to))
        elif end_time_from:
            query = query.where(InspectionRecord.end_time >= end_time_from)
        elif end_time_to:
            query = query.where(InspectionRecord.end_time <= end_time_to)

        # 排序和分页
        query = query.order_by(InspectionRecord.created_at.desc())
        pagination = db.paginate(
            select=query,
            page=page_num,
            per_page=page_size,
            max_per_page=100,
            error_out=False,
            count=True
        )

        inspections_data = []
        for inspection in pagination.items:
            # 获取执行工程师信息
            executor = None
            if inspection.executor_id:
                executor = db.session.get(User, inspection.executor_id)

            # 获取关联的任务、航班和飞机信息
            task = inspection.task
            flight = None
            aircraft = None

            if task:
                flight = db.session.get(Flight, task.flight_id)
                if flight and hasattr(flight, 'aircraft_id') and flight.aircraft_id:
                    aircraft = db.session.get(Aircraft, flight.aircraft_id)

            inspections_data.append(InspectionRecordDetailDTO(
                inspection_id=inspection.inspection_id,
                inspection_name=inspection.inspection_name,
                task_id=inspection.task_id,
                executor_id=inspection.executor_id,
                executor_name=executor.name if executor else None,
                reference_image_id=inspection.reference_image_id,
                reference_image_name=inspection.reference_image.image_name if inspection.reference_image else None,
                progress=inspection.progress,
                start_time=inspection.start_time,
                end_time=inspection.end_time,
                inspection_status=inspection.inspection_status,
                status_name=inspection.status_dict.dict_key,
                flight_id=flight.flight_id if flight else None,
                aircraft_id=flight.aircraft_id if flight and hasattr(flight, 'aircraft_id') else None,
                aircraft_name=aircraft.aircraft_name if aircraft else None,
                created_at=inspection.created_at,
                updated_at=inspection.updated_at
            ))

        pagination_dto = PaginationDTO(
            current_page=pagination.page,
            page_size=pagination.per_page,
            total=pagination.total or 0,
            total_pages=pagination.pages
        )

        response = InspectionRecordPagedResponseDTO(
            data=inspections_data,
            pagination=pagination_dto
        )
        return response
