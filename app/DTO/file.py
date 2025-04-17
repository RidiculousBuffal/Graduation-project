from typing import Optional

from pydantic import BaseModel


class FileDTO(BaseModel):
    download_url: Optional[str] = None
    filename: Optional[str] = None
    ipfs_cid: Optional[str] = None
    ipfs_path: Optional[str] = None
    mfs_path: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None
    stored_filename: Optional[str] = None
    success: Optional[bool] = None
    uploaded_at: Optional[str] = None
