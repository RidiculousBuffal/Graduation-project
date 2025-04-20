from typing import List, Optional

from pydantic import BaseModel

from app.DTO.pagination import PaginationDTO


class TerminalCreateDTO(BaseModel):
    terminal_name: str
    description: Optional[str] = None


class TerminalUpdateDTO(BaseModel):
    terminal_name: Optional[str] = None
    description: Optional[str] = None


class TerminalDTO(BaseModel):
    terminal_id: str
    terminal_name: str
    description: Optional[str] = None

class TerminalPagedResponseDTO(BaseModel):
    data: List[TerminalDTO]
    pagination: PaginationDTO
