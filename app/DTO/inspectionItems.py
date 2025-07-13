from datetime import datetime
from typing import Optional, List, Literal

from pydantic import BaseModel

from app.DTO.Base import BaseDTO
from app.DTO.aircrafts import AircraftReferenceImagePoint
from app.DTO.file import FileDTO
from app.DTO.pagination import PaginationDTO


class InspectionItemPointDTO(BaseDTO):
    point: AircraftReferenceImagePoint
    fileInfo: FileDTO


class YoloBoxDTO(BaseDTO):
    x1: float
    x2: float
    y1: float
    y2: float


class YoloDetect(BaseModel):
    points: Optional[YoloBoxDTO] = None
    label: Optional[str] = None
    confidence: Optional[float] = None


class YoloResult(BaseModel):
    boxes: Optional[List[YoloDetect]] = None
    resultImage: FileDTO


class InspectionItemResultDTO(BaseModel):
    resultImage: Optional[YoloResult] = None
    isPassed: Optional[bool] = False
    inputImage: FileDTO
    progress: Literal["pending", "detecting", "done", "canceled", "error"]
    version: int


class InspectionItemCreateDTO(BaseDTO):
    item_name: Optional[str] = None
    inspection_id: str
    item_point: Optional[InspectionItemPointDTO] = None
    result: Optional[List[InspectionItemResultDTO]] = []
    description: Optional[str] = None
    model_id: Optional[str] = None


class InspectionItemUpdateDTO(BaseDTO):
    item_name: Optional[str] = None
    inspection_id: Optional[str] = None
    item_point: Optional[InspectionItemPointDTO] = None
    description: Optional[str] = None
    result: Optional[List[InspectionItemResultDTO]] = []
    model_id: Optional[str] = None


class InspectionItemDTO(BaseDTO):
    item_id: str
    item_name: Optional[str] = None
    inspection_id: str
    item_point: Optional[InspectionItemPointDTO] = None
    description: Optional[str] = None
    result: Optional[List[InspectionItemResultDTO]] = []
    model_id: Optional[str] = None
    model_name: Optional[str] = None
    model_description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class InspectionItemPagedResponseDTO(BaseDTO):
    data: List[InspectionItemDTO]
    pagination: PaginationDTO
