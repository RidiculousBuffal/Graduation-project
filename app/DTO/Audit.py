from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel
from app.DTO.Base import BaseDTO
from app.DTO.pagination import PaginationDTO


class ActionDTO(BaseModel):
    userId: Optional[str] = None
    event_name: Optional[str] = None
    input_parameter: Optional[Any] = None
    result: Optional[Any] = None


class AuditLogDTO(BaseModel):
    action: ActionDTO
    blockchain_tx_hash: str
    blockchain_block_number: int
    blockchain_operator: str


class AuditLogSearchDTO(BaseDTO):
    log_id: Optional[int] = None
    user_id: Optional[str] = None
    action: Optional[ActionDTO] = None
    timestamp: Optional[datetime] = None
    blockchain_tx_hash: Optional[str] = None
    blockchain_block_number: Optional[int] = None
    blockchain_operator: Optional[str] = None


class AuditLogSearchResponsePaginationDTO(BaseDTO):
    data: list[AuditLogSearchDTO]
    pagination: PaginationDTO
