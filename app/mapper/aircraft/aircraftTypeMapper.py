from typing import Optional

from sqlalchemy import select, delete, update

from app.DTO.aircrafts import AircraftTypeCreateDTO, AircraftTypeDTO, AircraftTypeUpdateDTO, \
    AircraftTypePagedResponseDTO
from app.DTO.pagination import PaginationDTO
from app.ext.extensions import db
from app.models.aircraft import AircraftType


class AircraftTypeMapper:
    @staticmethod
    def create(aircraft_type_data: AircraftTypeCreateDTO):
        """创建AircraftType记录"""
        aircraft_type = AircraftType(
            type_name=aircraft_type_data.type_name,
            description=aircraft_type_data.description
        )
        db.session.add(aircraft_type)
        db.session.commit()
        return AircraftTypeDTO(
            typeid=aircraft_type.typeid,
            type_name=aircraft_type.type_name,
            description=aircraft_type.description
        )

    @staticmethod
    def get_by_id(typeid: str):
        """根据ID查询AircraftType记录"""
        aircraft_type = db.session.get(AircraftType, typeid)
        if aircraft_type:
            return AircraftTypeDTO(
                typeid=aircraft_type.typeid,
                type_name=aircraft_type.type_name,
                description=aircraft_type.description
            )
        return None

    @staticmethod
    def update(typeid: str, update_data: AircraftTypeUpdateDTO):
        """更新AircraftType记录"""
        aircraft_type = db.session.get(AircraftType, typeid)
        if not aircraft_type:
            return None

        if update_data.type_name is not None:
            aircraft_type.type_name = update_data.type_name
        if update_data.description is not None:
            aircraft_type.description = update_data.description

        db.session.commit()
        return AircraftTypeDTO(
            typeid=aircraft_type.typeid,
            type_name=aircraft_type.type_name,
            description=aircraft_type.description
        )

    @staticmethod
    def delete(typeid: str) -> bool:
        """删除AircraftType记录"""
        aircraft_type = db.session.get(AircraftType, typeid)
        if not aircraft_type:
            return False
        db.session.delete(aircraft_type)
        db.session.commit()
        return True

    @staticmethod
    def search(
            type_name: str = None,
            pageNum: int = 1,
            pageSize: int = 10
    ):
        """分页查询AircraftType记录"""
        query = select(AircraftType)
        if type_name:
            query = query.where(AircraftType.type_name == type_name)

        pagination = db.paginate(
            select=query,
            page=pageNum,
            per_page=pageSize,
            max_per_page=100,
            error_out=False,
            count=True
        )

        aircraft_types_data = []
        for aircraft_type in pagination.items:
            aircraft_types_data.append(AircraftTypeDTO(
                typeid=aircraft_type.typeid,
                type_name=aircraft_type.type_name,
                description=aircraft_type.description
            ))

        pagination_dto = PaginationDTO(
            current_page=pagination.page,
            page_size=pagination.per_page,
            total=pagination.total or 0,
            total_pages=pagination.pages
        )

        response = AircraftTypePagedResponseDTO(
            data=aircraft_types_data,
            pagination=pagination_dto
        )
        return response