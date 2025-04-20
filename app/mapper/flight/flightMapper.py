from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.DTO.flights import FlightCreateDTO, FlightUpdateDTO, FlightDTO, FlightDetailDTO, FlightPagedResponseDTO
from app.DTO.pagination import PaginationDTO
from app.ext.extensions import db
from app.models.flight import Flight

class FlightMapper:
    @staticmethod
    def create(flight_data: FlightCreateDTO) -> FlightDTO:
        """创建航班记录"""
        flight = Flight(
            aircraft_id=flight_data.aircraft_id,
            terminal_id=flight_data.terminal_id,
            estimated_departure=flight_data.estimated_departure,
            estimated_arrival=flight_data.estimated_arrival,
            flight_status=flight_data.flight_status,
            actual_departure=flight_data.actual_departure,
            actual_arrival=flight_data.actual_arrival,
            health_status=flight_data.health_status,
            approval_status=flight_data.approval_status
        )
        db.session.add(flight)
        db.session.commit()
        return FlightDTO.model_validate(flight)

    @staticmethod
    def get_by_id(flight_id: str) -> Optional[FlightDetailDTO]:
        """根据ID查询航班记录，包含详细信息"""
        # 使用 joinedload 加载关联的 aircraft 和 terminal
        flight = (db.session.query(Flight)
                  .options(joinedload(Flight.aircraft), joinedload(Flight.terminal))
                  .get(flight_id))
        if flight:
            # 手动构建 FlightDetailDTO，包含关联对象的名称
            return FlightDetailDTO(
                flight_id=flight.flight_id,
                aircraft_id=flight.aircraft_id,
                aircraft_name=flight.aircraft.aircraft_name if flight.aircraft else None,
                terminal_id=flight.terminal_id,
                terminal_name=flight.terminal.terminal_name if flight.terminal else None,
                estimated_departure=flight.estimated_departure,
                estimated_arrival=flight.estimated_arrival,
                flight_status=flight.flight_status,
                actual_departure=flight.actual_departure,
                actual_arrival=flight.actual_arrival,
                health_status=flight.health_status,
                approval_status=flight.approval_status,
                created_at=flight.created_at,
                updated_at=flight.updated_at
            )
        return None

    @staticmethod
    def update(flight_id: str, update_data: FlightUpdateDTO) -> Optional[FlightDTO]:
        """更新航班记录"""
        flight = db.session.get(Flight, flight_id)
        if not flight:
            return None

        if update_data.aircraft_id is not None:
            flight.aircraft_id = update_data.aircraft_id
        if update_data.terminal_id is not None:
            flight.terminal_id = update_data.terminal_id
        if update_data.estimated_departure is not None:
            flight.estimated_departure = update_data.estimated_departure
        if update_data.estimated_arrival is not None:
            flight.estimated_arrival = update_data.estimated_arrival
        if update_data.flight_status is not None:
            flight.flight_status = update_data.flight_status
        if update_data.actual_departure is not None:
            flight.actual_departure = update_data.actual_departure
        if update_data.actual_arrival is not None:
            flight.actual_arrival = update_data.actual_arrival
        if update_data.health_status is not None:
            flight.health_status = update_data.health_status
        if update_data.approval_status is not None:
            flight.approval_status = update_data.approval_status

        db.session.commit()
        return FlightDTO.model_validate(flight)

    @staticmethod
    def delete(flight_id: str) -> bool:
        """删除航班记录"""
        flight = db.session.get(Flight, flight_id)
        if not flight:
            return False
        db.session.delete(flight)
        db.session.commit()
        return True

    @staticmethod
    def search(
            aircraft_id: Optional[str] = None,
            terminal_id: Optional[str] = None,
            flight_status: Optional[str] = None,
            health_status: Optional[str] = None,
            approval_status: Optional[str] = None,
            pageNum: int = 1,
            pageSize: int = 10
    ) -> FlightPagedResponseDTO:
        """分页查询航班记录，包含详细信息"""
        query = select(Flight).options(joinedload(Flight.aircraft), joinedload(Flight.terminal))
        if aircraft_id:
            query = query.where(Flight.aircraft_id == aircraft_id)
        if terminal_id:
            query = query.where(Flight.terminal_id == terminal_id)
        if flight_status:
            query = query.where(Flight.flight_status == flight_status)
        if health_status:
            query = query.where(Flight.health_status == health_status)
        if approval_status:
            query = query.where(Flight.approval_status == approval_status)

        query = query.order_by(Flight.created_at.desc())
        pagination = db.paginate(
            select=query,
            page=pageNum,
            per_page=pageSize,
            max_per_page=100,
            error_out=False,
            count=True
        )

        # 手动构建 FlightDetailDTO 列表，包含关联对象的名称
        flights_data = []
        for flight in pagination.items:
            flights_data.append(FlightDetailDTO(
                flight_id=flight.flight_id,
                aircraft_id=flight.aircraft_id,
                aircraft_name=flight.aircraft.aircraft_name if flight.aircraft else None,
                terminal_id=flight.terminal_id,
                terminal_name=flight.terminal.terminal_name if flight.terminal else None,
                estimated_departure=flight.estimated_departure,
                estimated_arrival=flight.estimated_arrival,
                flight_status=flight.flight_status,
                actual_departure=flight.actual_departure,
                actual_arrival=flight.actual_arrival,
                health_status=flight.health_status,
                approval_status=flight.approval_status,
                created_at=flight.created_at,
                updated_at=flight.updated_at
            ))

        pagination_dto = PaginationDTO(
            current_page=pagination.page,
            page_size=pagination.per_page,
            total=pagination.total or 0,
            total_pages=pagination.pages
        )

        response = FlightPagedResponseDTO(
            data=flights_data,
            pagination=pagination_dto
        )
        return response