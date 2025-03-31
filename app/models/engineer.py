from app.ext.extensions import db
from datetime import datetime
import uuid


class Engineer(db.Model):
    __tablename__ = 'engineers'

    engineer_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.CHAR, comment='M-男, F-女')
    department = db.Column(db.String(100))
    work_years = db.Column(db.Integer)
    contact_info = db.Column(db.String(255))
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id', ondelete='SET NULL'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(),onupdate=datetime.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)

    # Relationships
    tasks = db.relationship('Task', backref='engineer', lazy='dynamic')
    inspection_records = db.relationship('InspectionRecord', backref='executor', lazy='dynamic')

    def __init__(self, **kwargs):
        if 'engineer_id' not in kwargs:
            kwargs['engineer_id'] = str(uuid.uuid4())
        super(Engineer, self).__init__(**kwargs)