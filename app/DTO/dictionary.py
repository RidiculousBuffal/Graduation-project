from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.DTO.pagination import PaginationDTO


class DictionaryDTO(BaseModel):
    dict_key: str
    dict_name: str
    description: Optional[str]
    parent_key: Optional[str]
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DictionaryDetailDTO(BaseModel):
    dict_key: str
    dict_name: str
    description: Optional[str]
    parent_key: Optional[str]
    sort_order: int
    created_at: datetime
    updated_at: datetime
    children: List['DictionaryDetailDTO'] = []  # 子字典项，嵌套结构

    model_config = ConfigDict(from_attributes=True)


class DictionaryPagedResponseDTO(BaseModel):
    data: List[DictionaryDetailDTO]
    pagination: PaginationDTO

    model_config = ConfigDict(from_attributes=True)
