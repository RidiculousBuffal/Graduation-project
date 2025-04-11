from typing import List, Optional

from pydantic import BaseModel

from app.DTO.pagination import PaginationDTO


class AircraftTypeDTO(BaseModel):
    typeid: str
    type_name: Optional[str] = None
    description: Optional[str] = None


class AircraftTypeCreateDTO(BaseModel):
    type_name: str
    description: Optional[str] = None


class AircraftTypeUpdateDTO(BaseModel):
    type_name: Optional[str] = None
    description: Optional[str] = None


class AircraftDTO(BaseModel):
    aircraft_id: str
    aircraft_name: Optional[str] = None
    age: Optional[int] = None
    typeid: Optional[str] = None
    type_name: Optional[str] = None
    type_description: Optional[str] = None


class AircraftCreateDTO(BaseModel):
    aircraft_name: str
    age: Optional[int] = None
    typeid: str


class AircraftUpdateDTO(BaseModel):
    aircraft_name: Optional[str] = None
    age: Optional[int] = None
    typeid: Optional[str] = None


class AircraftPagedResponseDTO(BaseModel):
    data: List[AircraftDTO]
    pagination: PaginationDTO


class AircraftTypePagedResponseDTO(BaseModel):
    data: List[AircraftTypeDTO]
    pagination: PaginationDTO
