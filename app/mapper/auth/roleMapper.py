from typing import Optional

from sqlalchemy import select
from app.DTO.user import Role as AuthRole
from app.models.auth import Role
from app.ext.extensions import db


class RoleMapper:
    @staticmethod
    def getRole(roleName: str) -> Optional[Role]:
        q = select(Role).where(Role.role_name == roleName)
        role = db.session.execute(q).scalar_one()
        return role

    @staticmethod
    def getAllRoles():
        q = select(Role)
        roles = db.session.execute(q).scalars()
        return [AuthRole(role_id=r.role_id, role_name=r.role_name, description=r.description) for r in roles]

    @staticmethod
    def createNewRole(roleName: str, description: Optional[str] = None):
        role = Role(role_name=roleName, description=description)
        db.session.add(role)
        db.session.commit()
        return role

    @staticmethod
    def deleteRole(roleId: int):
        role = db.session.get(Role, roleId)
        if role:
            db.session.delete(role)
        return True
