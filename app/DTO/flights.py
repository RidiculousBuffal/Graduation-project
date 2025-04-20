from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.DTO.pagination import PaginationDTO


class FlightCreateDTO(BaseModel):
    aircraft_id: str
    terminal_id: Optional[str] = None
    estimated_departure: Optional[datetime] = None
    estimated_arrival: Optional[datetime] = None
    flight_status: Optional[str] = "scheduled"  # 默认值：已排班
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    health_status: Optional[str] = "healthy"  # 默认值：健康
    approval_status: Optional[str] = "pending"  # 默认值：待审批

    # reference https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.validate_assignment
    model_config = ConfigDict(from_attributes=True, json_encoders={
        datetime: lambda v: v.isoformat() if v else None
    })  # 测试一下pydantic v2 新特性


class FlightUpdateDTO(BaseModel):
    aircraft_id: Optional[str] = None
    terminal_id: Optional[str] = None
    estimated_departure: Optional[datetime] = None
    estimated_arrival: Optional[datetime] = None
    flight_status: Optional[str] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    health_status: Optional[str] = None
    approval_status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, json_encoders={
        datetime: lambda v: v.isoformat() if v else None
    })  # 测试一下pydantic v2 新特性


class FlightDTO(BaseModel):
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

    model_config = ConfigDict(from_attributes=True, json_encoders={
        datetime: lambda v: v.isoformat() if v else None
    })  # 测试一下pydantic v2 新特性


class FlightDetailDTO(BaseModel):
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

    model_config = ConfigDict(from_attributes=True, json_encoders={
        datetime: lambda v: v.isoformat() if v else None
    })  # 测试一下pydantic v2 新特性


class FlightPagedResponseDTO(BaseModel):
    data: List[FlightDetailDTO]  # 使用 FlightDetailDTO 替代 FlightDTO
    pagination: PaginationDTO

    model_config = ConfigDict(from_attributes=True, json_encoders={
        datetime: lambda v: v.isoformat() if v else None
    })  # 测试一下pydantic v2 新特性
