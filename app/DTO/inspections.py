from datetime import datetime
from typing import Optional, List

from app.DTO.Base import BaseDTO
from app.DTO.pagination import PaginationDTO
from app.consts.Dict import DictionaryData


class InspectionRecordCreateDTO(BaseDTO):
    inspection_name: Optional[str] = None
    task_id: str
    executor_id: Optional[str] = None
    reference_image_id: Optional[str] = None
    progress: Optional[int] = 0
    start_time: Optional[datetime] = datetime.now()
    end_time: Optional[datetime] = None
    inspection_status: Optional[str] = DictionaryData.INSPECTION_NOT_STARTED.get('dict_key')


class InspectionRecordUpdateDTO(BaseDTO):
    inspection_name: Optional[str] = None
    task_id: Optional[str] = None
    executor_id: Optional[str] = None
    reference_image_id: Optional[str] = None
    progress: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    inspection_status: Optional[str] = None


class InspectionRecordDTO(BaseDTO):
    inspection_id: str
    inspection_name: Optional[str] = None
    task_id: str
    executor_id: Optional[str] = None
    reference_image_id: Optional[str] = None
    progress: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    inspection_status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class InspectionRecordDetailDTO(InspectionRecordDTO):
    executor_name: Optional[str] = None
    reference_image_name: Optional[str] = None
    status_name: Optional[str] = None
    flight_id: Optional[str] = None
    aircraft_id: Optional[str] = None
    aircraft_name: Optional[str] = None


class InspectionRecordPagedResponseDTO(BaseDTO):
    data: List[InspectionRecordDetailDTO]
    pagination: PaginationDTO
