import uuid
from datetime import datetime

from sqlalchemy_serializer import SerializerMixin

from app.ext.extensions import db


class Task(db.Model):
    __tablename__ = 'tasks'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    task_id = db.Column(db.String(50), primary_key=True)
    flight_id = db.Column(db.String(50), db.ForeignKey('flights.flight_id', ondelete='CASCADE'), nullable=False)
    estimated_start = db.Column(db.DateTime)
    estimated_end = db.Column(db.DateTime)
    actual_start = db.Column(db.DateTime)
    actual_end = db.Column(db.DateTime)
    admin_id = db.Column(db.String(50), db.ForeignKey('users.user_id', ondelete='SET NULL'))
    task_status = db.Column(db.String(50), db.ForeignKey('dictionary.dict_key'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)

    # Relationships
    status_dict = db.relationship('Dictionary', foreign_keys=[task_status])

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'flight_id': self.flight_id,
            'estimated_start': self.estimated_start,
            'estimated_end': self.estimated_end,
            'actual_start': self.actual_start,
            'actual_end': self.actual_end,
            'admin_id': self.admin_id,
            'task_status': self.task_status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def __init__(self, **kwargs):
        if 'task_id' not in kwargs:
            kwargs['task_id'] = str(uuid.uuid4())
        super(Task, self).__init__(**kwargs)
