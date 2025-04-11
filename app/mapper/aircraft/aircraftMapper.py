from sqlalchemy import select

from app.DTO.aircrafts import AircraftDTO, AircraftCreateDTO, AircraftUpdateDTO, AircraftPagedResponseDTO
from app.DTO.pagination import PaginationDTO
from app.ext.extensions import db
from app.models.aircraft import Aircraft, AircraftType


class AircraftMapper:
    @staticmethod
    def create(aircraft_data: AircraftCreateDTO):
        """创建Aircraft记录"""
        aircraft = Aircraft(
            aircraft_name=aircraft_data.aircraft_name,
            age=aircraft_data.age,
            typeid=aircraft_data.typeid
        )
        db.session.add(aircraft)
        db.session.commit()

        # 查询关联的 AircraftType 信息
        aircraft_type = db.session.get(AircraftType, aircraft.typeid)
        return AircraftDTO(
            aircraft_id=aircraft.aircraft_id,
            aircraft_name=aircraft.aircraft_name,
            age=aircraft.age,
            typeid=aircraft.typeid,
            type_name=aircraft_type.type_name if aircraft_type else None,
            type_description=aircraft_type.description if aircraft_type else None
        )

    @staticmethod
    def get_by_id(aircraft_id: str):
        """根据ID查询Aircraft记录"""
        aircraft = db.session.get(Aircraft, aircraft_id)
        if aircraft:
            aircraft_type = db.session.get(AircraftType, aircraft.typeid)
            return AircraftDTO(
                aircraft_id=aircraft.aircraft_id,
                aircraft_name=aircraft.aircraft_name,
                age=aircraft.age,
                typeid=aircraft.typeid,
                type_name=aircraft_type.type_name if aircraft_type else None,
                type_description=aircraft_type.description if aircraft_type else None
            )
        return None

    @staticmethod
    def update(aircraft_id: str, update_data: AircraftUpdateDTO):
        """更新Aircraft记录"""
        aircraft = db.session.get(Aircraft, aircraft_id)
        if not aircraft:
            return None

        if update_data.aircraft_name is not None:
            aircraft.aircraft_name = update_data.aircraft_name
        if update_data.age is not None:
            aircraft.age = update_data.age
        if update_data.typeid is not None:
            aircraft.typeid = update_data.typeid

        db.session.commit()

        aircraft_type = db.session.get(AircraftType, aircraft.typeid)
        return AircraftDTO(
            aircraft_id=aircraft.aircraft_id,
            aircraft_name=aircraft.aircraft_name,
            age=aircraft.age,
            typeid=aircraft.typeid,
            type_name=aircraft_type.type_name if aircraft_type else None,
            type_description=aircraft_type.description if aircraft_type else None
        )

    @staticmethod
    def delete(aircraft_id: str) -> bool:
        """删除Aircraft记录"""
        aircraft = db.session.get(Aircraft, aircraft_id)
        if not aircraft:
            return False
        db.session.delete(aircraft)
        db.session.commit()
        return True

    @staticmethod
    def searchAircraft(
            aircraftName: str = None,
            aircraftAge: str = None,
            aircraftTypeName: str = None,
            pageNum: int = 1,
            pageSize: int = 10
    ):
        """分页查询Aircraft记录"""
        query = (
            select(Aircraft, AircraftType.type_name, AircraftType.description)
            .join(AircraftType)
        )
        print(query)

        conditions = []
        if aircraftName:
            conditions.append(Aircraft.aircraft_name == aircraftName)
        if aircraftAge:
            conditions.append(Aircraft.age == int(aircraftAge))
        if aircraftTypeName:
            conditions.append(AircraftType.type_name == aircraftTypeName)

        if conditions:
            query = query.where(*conditions)

        pagination = db.paginate(
            select=query,
            page=pageNum,
            per_page=pageSize,
            max_per_page=100,
            error_out=False,
            count=True
        )

        aircraft_data = []
        # 打个断点,调试看看就是到是什么值了
        for item in pagination.items:
            aircraft_data.append(AircraftDTO(
                aircraft_id=item.aircraft_id,
                aircraft_name=item.aircraft_name,
                age=item.age,
                typeid=item.typeid,
                type_name=item.type.type_name,
                type_description=item.type.description
            ))

        pagination_dto = PaginationDTO(
            current_page=pagination.page,
            page_size=pagination.per_page,
            total=pagination.total or 0,
            total_pages=pagination.pages
        )

        response = AircraftPagedResponseDTO(
            data=aircraft_data,
            pagination=pagination_dto
        )
        return response
