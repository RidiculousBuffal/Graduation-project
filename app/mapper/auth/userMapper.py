from datetime import datetime
from typing import Optional

from sqlalchemy import select, update

from app.DTO.user import UserDTO
from app.ext.extensions import db
from app.models.auth import User, Role, UserRole


class UserMapper:
    @staticmethod
    def get_user_by_name(username: str) -> Optional[User]:
        q = select(User).where(User.username == username)
        user = db.session.execute(q).scalar_one_or_none()
        return user

    @staticmethod
    def updatePassword(user_id: str, hashed_pass: str):
        u = update(User).where(User.user_id == user_id).values(password=hashed_pass)
        db.session.execute(u)
        db.session.commit()
        return True

    @staticmethod
    def get_user_by_user_id(user_id: str) -> Optional[User]:
        q = select(User).where(User.user_id == user_id)
        user = db.session.execute(q).scalar_one_or_none()
        return user

    @staticmethod
    def update_user_basic_info(user: UserDTO, user_id: str):
        u = update(User).where(User.user_id == user_id).values(email=user.email, phone=user.phone, name=user.name,
                                                               gender=user.gender, department=user.department,
                                                               work_years=user.work_years, faceInfo=user.faceInfo)
        db.session.execute(u)
        db.session.commit()
        return True

    @staticmethod
    def update_user_face_login_info(user_id: str, b64: str):
        q = update(User).where(User.user_id == user_id).values(faceInfo=b64)
        db.session.execute(q)
        db.session.commit()

    @staticmethod
    def update_last_login(user_id: str):
        q = select(User).where(User.user_id == user_id)
        user = db.session.execute(q).scalar_one_or_none()
        if user:
            # 只更新last_login字段，不影响create_at
            db.session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(last_login=datetime.now())
            )
            db.session.commit()

    @staticmethod
    def validate_email(email: str):
        if not email:
            return True  # 邮箱可以是空
        q = select(User).where(User.email == email)
        user = db.session.execute(q).scalar_one_or_none()
        return user is None

    @staticmethod
    def validate_username(username: str) -> bool:
        q = select(User).where(User.username == username)
        user = db.session.execute(q).scalar_one_or_none()
        return user is None

    @staticmethod
    def add_user(username, password, email):
        user = User(username=username, password=password, email=email, name=username)
        db.session.add(user)
        db.session.commit()
        return user.user_id

    @staticmethod
    def delete_user(user_id: str):
        q = select(User).where(User.user_id == user_id)
        user = db.session.execute(q).scalar_one_or_none()
        if user:
            db.session.delete(user)
            db.session.commit()

    @staticmethod
    def get_users_by_role(role_name: str):

        q = (select(User).join(UserRole, User.user_id == UserRole.user_id)
             .join(Role, UserRole.role_id == Role.role_id)
             .where(Role.role_name == role_name))
        users = db.session.execute(q).scalars().all()
        return [u.to_dict() for u in users]
