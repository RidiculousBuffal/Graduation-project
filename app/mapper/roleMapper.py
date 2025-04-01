from typing import Optional

from sqlalchemy import select

from app.models.auth import Role
from app.ext.extensions import db
class RoleMapper:
    @staticmethod
    def getRole(roleName: str) -> Optional[Role]:
        q = select(Role).where(Role.role_name==roleName)
        role = db.session.execute(q).scalar_one()
        return role
