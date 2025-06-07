from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.DTO.pagination import PaginationDTO
from app.consts.Dict import DictionaryData


class TaskCreateDTO(BaseModel):
    flight_id: str
    estimated_start: Optional[datetime] = None
    estimated_end: Optional[datetime] = None
    admin_id: Optional[str] = None
    task_status: Optional[str] = DictionaryData.TASK_PENDING.get('dict_key')


class TaskUpdateDTO(BaseModel):
    flight_id: Optional[str] = None
    estimated_start: Optional[datetime] = None
    estimated_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    admin_id: Optional[str] = None
    task_status: Optional[str] = None


class TaskDTO(BaseModel):
    task_id: str
    flight_id: str
    estimated_start: Optional[datetime] = None
    estimated_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    admin_id: Optional[str] = None
    task_status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TaskDetailDTO(TaskDTO):
    aircraft_id: Optional[str] = None
    aircraft_name: Optional[str] = None
    admin_name: Optional[str] = None


class TaskPagedResponseDTO(BaseModel):
    data: List[TaskDetailDTO]
    pagination: PaginationDTO
