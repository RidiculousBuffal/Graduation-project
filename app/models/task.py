from app.ext.extensions import db
from datetime import datetime
import uuid


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.String(50), primary_key=True)
    flight_id = db.Column(db.String(50), db.ForeignKey('flights.flight_id', ondelete='CASCADE'), nullable=False)
    estimated_start = db.Column(db.DateTime)
    estimated_end = db.Column(db.DateTime)
    actual_start = db.Column(db.DateTime)
    actual_end = db.Column(db.DateTime)
    engineer_id = db.Column(db.String(50), db.ForeignKey('engineers.engineer_id', ondelete='SET NULL'))
    task_status = db.Column(db.String(50), db.ForeignKey('dictionary.dict_key'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(),onupdate=datetime.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)

    # Relationships
    status_dict = db.relationship('Dictionary', foreign_keys=[task_status])

    def __init__(self, **kwargs):
        if 'task_id' not in kwargs:
            kwargs['task_id'] = str(uuid.uuid4())
        super(Task, self).__init__(**kwargs)