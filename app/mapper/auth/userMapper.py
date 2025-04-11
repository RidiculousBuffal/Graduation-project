from datetime import datetime
from typing import Optional

from sqlalchemy import select

from app.ext.extensions import db
from app.models.auth import User


class UserMapper:
    @staticmethod
    def get_user_by_name(username: str) -> Optional[User]:
        q = select(User).where(User.username == username)
        user = db.session.execute(q).scalar_one_or_none()
        return user

    @staticmethod
    def update_last_login(user_id: str):
        q = select(User).where(User.user_id == user_id)
        user = db.session.execute(q).scalar_one_or_none()
        if user:
            user.last_login = datetime.now()
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
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return user.user_id
