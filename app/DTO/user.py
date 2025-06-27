from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.DTO.Base import BaseDTO
from app.DTO.pagination import PaginationDTO


class UserDTO(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[str] = None
    work_years: Optional[int] = None
    department: Optional[str] = None
    faceInfo: Optional[str] = None
    userId:Optional[str] = None


class ResetPasswordDTO(BaseModel):
    password: Optional[str] = None
    newPassword: Optional[str] = None


class Role(BaseModel):
    role_id: Optional[int] = None
    role_name: Optional[str] = None
    description: Optional[str] = None





class Permission(BaseModel):
    permission_id: Optional[int] = None
    permission_name: Optional[str] = None
    description: Optional[str] = None


class RolePermissionDTO(BaseModel):
    role: Role
    permissions: List[Permission]


class createRoleDTO(BaseModel):
    role_name: str
    description: Optional[str] = None


class AdminUserDTO(BaseDTO):
    user_id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    faceInfo: Optional[str] = None
    status: Optional[bool] = None
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: Optional[str] = None
    gender: Optional[str] = None
    department: Optional[str] = None
    work_years: Optional[int] = None
    contact_info: Optional[str] = None


class AdminUserDTOWithRolesAndPermissions(AdminUserDTO):
    roles: Optional[list[Role]] = []
    permissions: Optional[list[Permission]] = []


class AdminUserPaginationDTO(BaseDTO):
    data: list[AdminUserDTOWithRolesAndPermissions]
    pagination: PaginationDTO
