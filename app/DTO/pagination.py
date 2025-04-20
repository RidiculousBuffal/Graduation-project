from pydantic import BaseModel


class PaginationDTO(BaseModel):
    current_page: int
    page_size: int
    total: int
    total_pages: int
    model_config = {"from_attributes": True}