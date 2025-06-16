from typing import List, Optional

from pydantic import BaseModel

from app.DTO.pagination import PaginationDTO
from app.DTO.file import FileDTO

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

class AircraftCallBackDTO(BaseModel):
    aircraft_id: str
    aircraft_name: Optional[str] = None
    age: Optional[int] = None
    typeid: Optional[str] = None
    type_name: Optional[str] = None
    description: Optional[str] = None

class AircraftCreateDTO(BaseModel):
    aircraft_name: str
    age: Optional[int] = None
    typeid: str


class AircraftUpdateDTO(BaseModel):
    aircraft_name: Optional[str] = None
    age: Optional[int] = None
    typeid: Optional[str] = None


class AircraftPagedResponseDTO(BaseModel):
    data: List[AircraftCallBackDTO]
    pagination: PaginationDTO


class AircraftTypePagedResponseDTO(BaseModel):
    data: List[AircraftTypeDTO]
    pagination: PaginationDTO


class AircraftReferenceImagePoint(BaseModel):
    id: Optional[int] = None
    x: Optional[float] = None
    y: Optional[float] = None


class AircraftReferenceImageJson(BaseModel):

    fileInfo: FileDTO
    pointInfo: List[AircraftReferenceImagePoint]


class AircraftReferenceImageDTO(BaseModel):
    image_id: str
    image_name: str
    image_description: str
    image_json: AircraftReferenceImageJson
    aircraft_id: str
    aircraft_name: Optional[str] = None  # 新增 aircraft_name 字段

class AircraftReferenceImageCreateDTO(BaseModel):
    image_name: str
    image_description: Optional[str]=None
    image_json: AircraftReferenceImageJson
    aircraft_id: str

class AircraftReferenceImageUpdateDTO(BaseModel):
    image_name: Optional[str] = None
    image_description: Optional[str] = None
    image_json: Optional[AircraftReferenceImageJson] = None
    aircraft_id: Optional[str] = None

class AircraftReferenceImagePagedResponseDTO(BaseModel):
    data: List[AircraftReferenceImageDTO]
    pagination: PaginationDTO