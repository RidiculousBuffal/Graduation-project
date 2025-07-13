from typing import List, Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.DTO.inspectionItems import (
    InspectionItemCreateDTO,
    InspectionItemUpdateDTO,
    InspectionItemDTO, InspectionItemPagedResponseDTO
)
from app.DTO.pagination import PaginationDTO
from app.ext.extensions import db
from app.models.inspection import InspectionItem


class InspectionItemMapper:
    @staticmethod
    def create(data: InspectionItemCreateDTO) -> InspectionItemDTO:
        item_point = data.item_point.model_dump()
        item = InspectionItem(
            item_name=data.item_name,
            inspection_id=data.inspection_id,
            item_point=item_point,
            result=[x.model_dump() for x in data.result],
            description=data.description,
            model_id=data.model_id
        )
        db.session.add(item)
        db.session.commit()

        # SerializerMixin.to_dict() 会返回基础字段和值
        return InspectionItemDTO.model_validate(item.to_dict())

    @staticmethod
    def get_by_id(item_id: str) -> Optional[InspectionItemDTO]:
        """根据主键获取一个 InspectionItem"""
        item = db.session.get(InspectionItem, item_id)
        if not item:
            return None
        return InspectionItemDTO.model_validate(item.to_dict())

    @staticmethod
    def update(item_id: str, data: InspectionItemUpdateDTO) -> Optional[InspectionItemDTO]:
        """更新 InspectionItem"""
        item = db.session.get(InspectionItem, item_id)
        if not item:
            return None

        if data.item_name is not None:
            item.item_name = data.item_name
        if data.inspection_id is not None:
            item.inspection_id = data.inspection_id
        if data.item_point is not None:
            item.item_point = data.item_point.model_dump()
        if data.description is not None:
            item.description = data.description
        if data.result is not None and data.result is not []:
            item.result = [r.model_dump() for r in data.result]
        if data.model_id is not None:
            item.model_id = data.model_id

        item.updated_at = datetime.now()
        db.session.commit()
        return InspectionItemDTO.model_validate(item.to_dict())

    @staticmethod
    def delete(item_id: str) -> bool:
        """删除 InspectionItem"""
        item = db.session.get(InspectionItem, item_id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    @staticmethod
    def list_by_inspection_id(
            inspection_id: str,
            page_num: int = 1,
            page_size: int = 10
    ) -> InspectionItemPagedResponseDTO:
        query = (
            select(InspectionItem)
            .options(joinedload(InspectionItem.model))
            .filter(InspectionItem.inspection_id == inspection_id)
            .order_by(InspectionItem.created_at.asc())
        )

        # 使用 db.paginate 进行分页查询
        pagination = db.paginate(
            select=query,
            page=page_num,
            per_page=page_size,
            max_per_page=100,
            error_out=False,
            count=True
        )

        dto_list = []
        for item in pagination.items:
            # 这部分逻辑保持不变
            base = item.to_dict()
            if item.model:
                base['model_name'] = item.model.model_name
                base['model_description'] = item.model.model_description
            else:
                base['model_name'] = None
                base['model_description'] = None

            dto = InspectionItemDTO.model_validate(base)
            dto_list.append(dto)

        # 创建分页信息 DTO
        pagination_dto = PaginationDTO(
            current_page=pagination.page,
            page_size=pagination.per_page,
            total=pagination.total or 0,
            total_pages=pagination.pages or 0
        )

        # 封装到最终的分页响应 DTO 中
        return InspectionItemPagedResponseDTO(
            data=dto_list,
            pagination=pagination_dto
        )
