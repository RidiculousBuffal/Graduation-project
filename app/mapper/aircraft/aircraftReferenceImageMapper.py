from typing import Optional

from sqlalchemy import select

from app.DTO.aircrafts import AircraftReferenceImageCreateDTO, AircraftReferenceImageDTO, AircraftReferenceImageJson, \
    AircraftReferenceImageUpdateDTO, AircraftReferenceImagePagedResponseDTO
from app.DTO.pagination import PaginationDTO
from app.ext.extensions import db
from app.models.aircraft import AircraftReferenceImage, Aircraft


class AircraftReferenceImageMapper:
    @staticmethod
    def create(image_data: AircraftReferenceImageCreateDTO) -> AircraftReferenceImageDTO:
        """创建 AircraftReferenceImage 记录"""
        image = AircraftReferenceImage(
            image_name=image_data.image_name,
            image_description=image_data.image_description,
            image_json=image_data.image_json.model_dump(),  # 将 Pydantic 模型转为字典存储为 JSON
            aircraft_id=image_data.aircraft_id
        )
        db.session.add(image)
        db.session.commit()

        return AircraftReferenceImageDTO(
            image_id=image.image_id,
            image_name=image.image_name,
            image_description=image.image_description,
            image_json=image_data.image_json,  # 直接使用传入的 Pydantic 模型
            aircraft_id=image.aircraft_id
        )

    @staticmethod
    def get_by_id(image_id: str) -> Optional[AircraftReferenceImageDTO]:
        """根据 ID 查询 AircraftReferenceImage 记录"""
        image = db.session.get(AircraftReferenceImage, image_id)
        if image:
            return AircraftReferenceImageDTO(
                image_id=image.image_id,
                image_name=image.image_name,
                image_description=image.image_description,
                image_json=AircraftReferenceImageJson.model_validate(image.image_json),
                aircraft_id=image.aircraft_id
            )
        return None

    @staticmethod
    def update(image_id: str, update_data: AircraftReferenceImageUpdateDTO) -> Optional[AircraftReferenceImageDTO]:
        """更新 AircraftReferenceImage 记录"""
        image = db.session.get(AircraftReferenceImage, image_id)
        if not image:
            return None

        if update_data.image_name is not None:
            image.image_name = update_data.image_name
        if update_data.image_description is not None:
            image.image_description = update_data.image_description
        if update_data.image_json is not None:
            image.image_json = update_data.image_json.model_dump()  # 将 Pydantic 模型转为字典
        if update_data.aircraft_id is not None:
            image.aircraft_id = update_data.aircraft_id

        db.session.commit()

        return AircraftReferenceImageDTO(
            image_id=image.image_id,
            image_name=image.image_name,
            image_description=image.image_description,
            image_json=AircraftReferenceImageJson.model_validate(image.image_json),
            aircraft_id=image.aircraft_id
        )

    @staticmethod
    def delete(image_id: str) -> bool:
        """删除 AircraftReferenceImage 记录"""
        image = db.session.get(AircraftReferenceImage, image_id)
        if not image:
            return False
        db.session.delete(image)
        db.session.commit()
        return True

    @staticmethod
    def search(
            image_name: Optional[str] = None,
            aircraft_id: Optional[str] = None,
            aircraft_name: Optional[str] = None,  # 新增 aircraft_name 作为搜索条件
            page_num: int = 1,
            page_size: int = 10
    ) -> AircraftReferenceImagePagedResponseDTO:
        """分页查询 AircraftReferenceImage 记录，支持通过 aircraft_name 搜索"""
        query = (
            select(AircraftReferenceImage, Aircraft.aircraft_name)
            .outerjoin(Aircraft)
        )
        conditions = []
        if image_name:
            conditions.append(AircraftReferenceImage.image_name.ilike(f"%{image_name}%"))
        if aircraft_id:
            conditions.append(AircraftReferenceImage.aircraft_id == aircraft_id)
        if aircraft_name:
            conditions.append(Aircraft.aircraft_name.ilike(f"%{aircraft_name}%"))
        if conditions:
            query = query.where(*conditions)
        query = query.order_by(AircraftReferenceImage.image_id)
        pagination = db.paginate(
            select=query,
            page=page_num,
            per_page=page_size,
            max_per_page=100,
            error_out=False,
            count=True
        )

        image_data = []
        for item in pagination.items:
            image_data.append(AircraftReferenceImageDTO(
                image_id=item.image_id,
                image_name=item.image_name,
                image_description=item.image_description,
                image_json=AircraftReferenceImageJson.model_validate(item.image_json),
                aircraft_id=item.aircraft_id,
                aircraft_name=item.aircraft.aircraft_name if hasattr(item, 'aircraft') else None
            ))

        pagination_dto = PaginationDTO(
            current_page=pagination.page,
            page_size=pagination.per_page,
            total=pagination.total or 0,
            total_pages=pagination.pages
        )

        response = AircraftReferenceImagePagedResponseDTO(
            data=image_data,
            pagination=pagination_dto
        )
        return response
