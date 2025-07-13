from typing import Optional

from app.DTO.Base import BaseDTO


class ModelDTO(BaseDTO):
    model_id: Optional[str] = None
    model_name: Optional[str] = None
    model_description: Optional[str] = None
    model_api_path:Optional[str] = None