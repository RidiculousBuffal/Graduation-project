import uuid
from datetime import datetime

from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.ext.extensions import db


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    user_id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    faceInfo = db.Column(db.Text, comment='人脸数据信息,可以是人脸的url链接,json等')
    status = db.Column(db.Boolean, default=True, comment='1-启用, 0-禁用')
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)

    # Relationships
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    engineers = db.relationship('Engineer', backref='user', lazy='dynamic')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')

    serialize_rules = ('-password', '-roles', '-engineers', '-audit_logs')

    def __init__(self, **kwargs):
        if 'user_id' not in kwargs:
            kwargs['user_id'] = str(uuid.uuid4())
        if 'password' in kwargs:
            kwargs['password'] = generate_password_hash(kwargs['password'])
        super(User, self).__init__(**kwargs)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(db.Model, SerializerMixin):
    __tablename__ = 'roles'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)

    # Relationships
    permissions = db.relationship('Permission', secondary='role_permissions',
                                  backref=db.backref('roles', lazy='dynamic'))
    serialize_rules = ('-permissions',)


class Permission(db.Model, SerializerMixin):
    __tablename__ = 'permissions'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)


class UserRole(db.Model, SerializerMixin):
    __tablename__ = 'user_roles'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id', ondelete='CASCADE'), primary_key=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    def __init__(self, **kwargs):
        super(UserRole, self).__init__(**kwargs)


class RolePermission(db.Model, SerializerMixin):
    __tablename__ = 'role_permissions'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id', ondelete='CASCADE'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.permission_id', ondelete='CASCADE'),
                              primary_key=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now(), onupdate=datetime.now(), nullable=False)
