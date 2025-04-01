from datetime import datetime
from typing import Optional

from app.ext.extensions import db
from app.models.auth import User


class UserMapper:
    @staticmethod
    def get_user_by_name(username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def update_last_login(user_id: str):
        user: User = User.query.get(user_id)
        if user:
            user.last_login = datetime.now()
            db.session.commit()

    @staticmethod
    def validate_email(email: str):
        if not email:
            return True  # 邮箱可以是空
        return User.query.filter_by(email=email).first() is None

    @staticmethod
    def validate_username(username: str) -> bool:
        return User.query.filter_by(username=username).first() is None

    @staticmethod
    def add_user(username,password,email):
        user = User(username=username,password=password,email=email)
        db.session.add(user)
        db.session.commit()
        return user.user_id
