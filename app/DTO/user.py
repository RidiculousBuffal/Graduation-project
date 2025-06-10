from typing import Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[str] = None
    work_years: Optional[int] = None
    department: Optional[str] = None
    faceInfo: Optional[str] = None


class ResetPasswordDTO(BaseModel):
    password: Optional[str] = None
    newPassword: Optional[str] = None
