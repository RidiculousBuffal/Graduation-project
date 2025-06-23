from datetime import datetime
from typing import Optional

from sqlalchemy import select, between
from sqlalchemy.orm import joinedload

from app.DTO.aircrafts import AircraftReferenceImageJson
from app.DTO.flights import FlightCreateDTO, FlightUpdateDTO, FlightDTO, FlightDetailDTO, FlightPagedResponseDTO, \
    FlightAircraftImageDTO
from app.DTO.pagination import PaginationDTO
from app.exceptions.flights import FlightTimeConflictError, FlightTimestampOrderError, FlightActualVsEstimatedError
from app.ext.extensions import db
from app.models import Aircraft, Terminal
from app.models.aircraft import AircraftReferenceImage
from app.models.flight import Flight
from app.utils.timeUtils import parse_to_utc


class FlightMapper:
    @staticmethod
    def _check_time_conflict(aircraft_id: str, estimated_departure: datetime, estimated_arrival: datetime,
                             exclude_flight_id: Optional[str] = None) -> bool:
        """检查在指定时间区间内，是否有其他使用相同 aircraft_id 的航班"""
        if not estimated_departure or not estimated_arrival:
            return False  # 如果时间为空，则不检查冲突

        # 查询条件：时间区间重叠
        # (start1 <= end2) AND (end1 >= start2) 表示两个时间段有重叠
        query = db.session.query(Flight).filter(
            Flight.aircraft_id == aircraft_id,
            Flight.estimated_departure <= estimated_arrival,
            Flight.estimated_arrival >= estimated_departure
        )
        if exclude_flight_id:
            query = query.filter(Flight.flight_id != exclude_flight_id)

        conflict_flight = query.first()
        return conflict_flight is not None

    @staticmethod
    def _validate_timestamps(start_time: Optional[datetime], end_time: Optional[datetime], field_name: str) -> None:
        """验证结束时间是否晚于开始时间"""
        if start_time and end_time and end_time < start_time:
            raise FlightTimestampOrderError(f"{field_name}到达时间不能早于起飞时间。")

    @staticmethod
    def _validate_actual_vs_estimated(estimated: Optional[datetime], actual: Optional[datetime],
                                      field_name: str) -> None:
        """验证实际时间是否晚于预计时间"""
        if estimated and actual and actual < estimated:
            raise FlightActualVsEstimatedError(f"实际{field_name}时间不能早于预计{field_name}时间。")

    @staticmethod
    def create(flight_data: FlightCreateDTO) -> FlightDTO:
        """创建航班记录"""
        # 验证时间顺序
        FlightMapper._validate_timestamps(flight_data.estimated_departure, flight_data.estimated_arrival, "预计")
        FlightMapper._validate_timestamps(flight_data.actual_departure, flight_data.actual_arrival, "实际")
        FlightMapper._validate_actual_vs_estimated(flight_data.estimated_departure, flight_data.actual_departure,
                                                   "起飞")
        FlightMapper._validate_actual_vs_estimated(flight_data.estimated_arrival, flight_data.actual_arrival, "到达")

        # 检查时间冲突
        if flight_data.estimated_departure and flight_data.estimated_arrival:
            if FlightMapper._check_time_conflict(
                    aircraft_id=flight_data.aircraft_id,
                    estimated_departure=flight_data.estimated_departure,
                    estimated_arrival=flight_data.estimated_arrival
            ):
                raise FlightTimeConflictError("在指定时间区间内，该飞机已被安排其他航班，无法创建新的航班。")

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
        flight = (db.session.query(Flight)
                  .options(joinedload(Flight.aircraft), joinedload(Flight.terminal))
                  .get(flight_id))
        if flight:
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

        # 验证时间顺序
        estimated_departure = update_data.estimated_departure if update_data.estimated_departure is not None else flight.estimated_departure
        estimated_arrival = update_data.estimated_arrival if update_data.estimated_arrival is not None else flight.estimated_arrival
        actual_departure = update_data.actual_departure if update_data.actual_departure is not None else flight.actual_departure
        actual_arrival = update_data.actual_arrival if update_data.actual_arrival is not None else flight.actual_arrival

        FlightMapper._validate_timestamps(estimated_departure, estimated_arrival, "预计")
        FlightMapper._validate_timestamps(actual_departure, actual_arrival, "实际")
        FlightMapper._validate_actual_vs_estimated(estimated_departure, actual_departure, "起飞")
        FlightMapper._validate_actual_vs_estimated(estimated_arrival, actual_arrival, "到达")

        # 检查时间冲突
        if estimated_departure and estimated_arrival:
            if FlightMapper._check_time_conflict(
                    aircraft_id=update_data.aircraft_id if update_data.aircraft_id is not None else flight.aircraft_id,
                    estimated_departure=estimated_departure,
                    estimated_arrival=estimated_arrival,
                    exclude_flight_id=flight_id
            ):
                raise FlightTimeConflictError("在指定时间区间内，该飞机已被安排其他航班，无法更新航班时间。")

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
            aircraft_name: Optional[str] = None,
            terminal_name: Optional[str] = None,
            estimated_departure_start: Optional[str] = None,
            estimated_departure_end: Optional[str] = None,
            estimated_arrival_start: Optional[str] = None,
            estimated_arrival_end: Optional[str] = None,
            actual_departure_start: Optional[str] = None,
            actual_departure_end: Optional[str] = None,
            actual_arrival_start: Optional[str] = None,
            actual_arrival_end: Optional[str] = None,
            pageNum: int = 1,
            pageSize: int = 10
    ) -> FlightPagedResponseDTO:
        """分页查询航班记录，包含详细信息，支持按航站楼名称、飞机名称及时间段查询"""
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

        if aircraft_name:
            query = query.join(Aircraft)
            query = query.where(Aircraft.aircraft_name.ilike(f"%{aircraft_name}%"))

        if terminal_name:
            query = query.join(Terminal)
            query = query.where(Terminal.terminal_name.ilike(f"%{terminal_name}%"))

        est_dep_start = parse_to_utc(estimated_departure_start)
        est_dep_end = parse_to_utc(estimated_departure_end)
        est_arr_start = parse_to_utc(estimated_arrival_start)
        est_arr_end = parse_to_utc(estimated_arrival_end)
        act_dep_start = parse_to_utc(actual_departure_start)
        act_dep_end = parse_to_utc(actual_departure_end)
        act_arr_start = parse_to_utc(actual_arrival_start)
        act_arr_end = parse_to_utc(actual_arrival_end)

        # 查询条件
        if est_dep_start and est_dep_end:
            query = query.where(between(Flight.estimated_departure, est_dep_start, est_dep_end))
        elif est_dep_start:
            query = query.where(Flight.estimated_departure >= est_dep_start)
        elif est_dep_end:
            query = query.where(Flight.estimated_departure <= est_dep_end)

        if est_arr_start and est_arr_end:
            query = query.where(between(Flight.estimated_arrival, est_arr_start, est_arr_end))
        elif est_arr_start:
            query = query.where(Flight.estimated_arrival >= est_arr_start)
        elif est_arr_end:
            query = query.where(Flight.estimated_arrival <= est_arr_end)

        if act_dep_start and act_dep_end:
            query = query.where(between(Flight.actual_departure, act_dep_start, act_dep_end))
        elif act_dep_start:
            query = query.where(Flight.actual_departure >= act_dep_start)
        elif act_dep_end:
            query = query.where(Flight.actual_departure <= act_dep_end)

        if act_arr_start and act_arr_end:
            query = query.where(between(Flight.actual_arrival, act_arr_start, act_arr_end))
        elif act_arr_start:
            query = query.where(Flight.actual_arrival >= act_arr_start)
        elif act_arr_end:
            query = query.where(Flight.actual_arrival <= act_arr_end)

        # 其他不变
        query = query.order_by(Flight.created_at.desc())
        pagination = db.paginate(
            select=query,
            page=pageNum,
            per_page=pageSize,
            max_per_page=100,
            error_out=False,
            count=True
        )

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

    @staticmethod
    def get_all_related_aircraft_image_by_flight_id(flight_id: str):
        # 1. 查询（一次提取出 flight_id、aircraft_id、aircraft_name、参考图像相关所有字段）
        query = (
            db.session.query(
                Flight.flight_id,
                Aircraft.aircraft_id,
                Aircraft.aircraft_name,
                AircraftReferenceImage.image_id.label('aircraft_image_id'),
                AircraftReferenceImage.image_json.label('aircraft_image_json')
            )
            .join(Aircraft, Flight.aircraft_id == Aircraft.aircraft_id)
            .join(AircraftReferenceImage, AircraftReferenceImage.aircraft_id == Aircraft.aircraft_id)
            .filter(Flight.flight_id == flight_id)
        )
        rows = query.all()

        # 2. 组装 DTO 列表
        result_list = []
        for row in rows:
            image_json = row.aircraft_image_json
            if image_json:
                try:
                    arij = AircraftReferenceImageJson.model_validate(image_json)
                except Exception as e:
                    arij = None
            else:
                arij = None
            dto = FlightAircraftImageDTO(
                aircraft_id=row.aircraft_id,
                aircraft_name=row.aircraft_name,
                aircraft_image_id=row.aircraft_image_id,
                aircraft_image_json=arij,
                flight_id=row.flight_id
            )
            result_list.append(dto)
        return result_list


if __name__ == '__main__':
    from app import create_app

    fake_app = create_app()
    with fake_app.app_context():
        FlightMapper.get_all_related_aircraft_image_by_flight_id("4ed86373-b98c-8730-2e6ca1514bd3")
