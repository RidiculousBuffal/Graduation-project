from pydantic import BaseModel, ConfigDict


class PaginationDTO(BaseModel):
    current_page: int
    page_size: int
    total: int
    total_pages: int
    model_config = ConfigDict(from_attributes=True)