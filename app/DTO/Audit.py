from typing import Optional, Any

from pydantic import BaseModel


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
