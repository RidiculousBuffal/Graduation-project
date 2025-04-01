from app.consts.Roles import RoleConsts


def initRoles():
    from sqlalchemy import inspect
    from app.ext.extensions import db
    inspector = inspect(db.engine)
    if 'roles' not in inspector.get_table_names():
        return
    from app.models.auth import Role
    existing_roles = {r.role_name for r in Role.query.all()}
    required_roles = {RoleConsts.ADMIN, RoleConsts.ENGINEER, RoleConsts.USER}
    for role_name in required_roles - existing_roles:
        description = {
            RoleConsts.ADMIN: "管理员,拥有全部权限",
            RoleConsts.USER: '普通用户',
            RoleConsts.ENGINEER: "工程师"
        }.get(role_name, '')
        db.session.add(Role(role_name=role_name, description=description))
    db.session.commit()
