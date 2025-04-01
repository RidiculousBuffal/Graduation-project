from typing import Optional

from app.models.auth import Role

class RoleMapper:
    @staticmethod
    def getRole(roleName: str) -> Optional[Role]:
        return Role.query.filter_by(role_name=roleName).first()
