from datetime import datetime
from typing import Optional, List

from app.DTO.Base import BaseDTO
from app.DTO.aircrafts import AircraftReferenceImageJson
from app.DTO.pagination import PaginationDTO


class FlightCreateDTO(BaseDTO):
    aircraft_id: str
    terminal_id: Optional[str] = None
    estimated_departure: Optional[datetime] = None
    estimated_arrival: Optional[datetime] = None
    flight_status: Optional[str] = "scheduled"  # 默认值：已排班
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    health_status: Optional[str] = "pending_check"  # 默认值：待检查
    approval_status: Optional[str] = "pending"  # 默认值：待审批


class FlightUpdateDTO(BaseDTO):
    aircraft_id: Optional[str] = None
    terminal_id: Optional[str] = None
    estimated_departure: Optional[datetime] = None
    estimated_arrival: Optional[datetime] = None
    flight_status: Optional[str] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    health_status: Optional[str] = None
    approval_status: Optional[str] = None


class FlightDTO(BaseDTO):
    flight_id: str
    aircraft_id: str
    terminal_id: Optional[str]
    estimated_departure: Optional[datetime]
    estimated_arrival: Optional[datetime]
    flight_status: Optional[str]
    actual_departure: Optional[datetime]
    actual_arrival: Optional[datetime]
    health_status: Optional[str]
    approval_status: Optional[str]
    created_at: datetime
    updated_at: datetime


class FlightDetailDTO(BaseDTO):
    flight_id: str
    aircraft_id: str
    aircraft_name: Optional[str]  # 飞机名称，从关联的 Aircraft 获取
    terminal_id: Optional[str]
    terminal_name: Optional[str]  # 航站楼名称，从关联的 Terminal 获取
    estimated_departure: Optional[datetime]
    estimated_arrival: Optional[datetime]
    flight_status: Optional[str]
    actual_departure: Optional[datetime]
    actual_arrival: Optional[datetime]
    health_status: Optional[str]
    approval_status: Optional[str]
    created_at: datetime
    updated_at: datetime


class FlightPagedResponseDTO(BaseDTO):
    data: List[FlightDetailDTO]  # 使用 FlightDetailDTO 替代 FlightDTO
    pagination: PaginationDTO


class FlightAircraftImageDTO(BaseDTO):
    aircraft_id: str
    aircraft_name: Optional[str] = None
    aircraft_image_id: str
    image_name: Optional[str] = None
    aircraft_image_json: Optional[AircraftReferenceImageJson]
    flight_id: str


class FlightWithAircraftName(BaseDTO):
    aircraft_id: Optional[str] = None
    aircraft_name: Optional[str] = None
    flight_id: Optional[str] = None
