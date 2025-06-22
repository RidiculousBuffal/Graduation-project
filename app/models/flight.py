import uuid
from datetime import datetime

from sqlalchemy_serializer import SerializerMixin

from app.ext.extensions import db


class Flight(db.Model, SerializerMixin):
    __tablename__ = 'flights'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    flight_id = db.Column(db.String(50), primary_key=True)
    aircraft_id = db.Column(db.String(50), db.ForeignKey('aircraft.aircraft_id'), nullable=False)
    terminal_id = db.Column(db.String(50), db.ForeignKey('terminal.terminal_id'))
    estimated_departure = db.Column(db.DateTime, comment='预计起飞')
    estimated_arrival = db.Column(db.DateTime, comment='预计到达')
    flight_status = db.Column(db.String(50), db.ForeignKey('dictionary.dict_key'))
    actual_departure = db.Column(db.DateTime, comment='实际起飞')
    actual_arrival = db.Column(db.DateTime, comment='实际到达')
    health_status = db.Column(db.String(50), db.ForeignKey('dictionary.dict_key'))
    approval_status = db.Column(db.String(50), db.ForeignKey('dictionary.dict_key'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)

    # Relationships
    terminal = db.relationship('Terminal', backref='flights')
    flight_status_dict = db.relationship('Dictionary', foreign_keys=[flight_status])
    health_status_dict = db.relationship('Dictionary', foreign_keys=[health_status])
    approval_status_dict = db.relationship('Dictionary', foreign_keys=[approval_status])
    tasks = db.relationship('Task', backref='flight', lazy='dynamic', cascade='all, delete-orphan',
                            passive_deletes=True)

    def __init__(self, **kwargs):
        if 'flight_id' not in kwargs:
            kwargs['flight_id'] = str(uuid.uuid4())
        super(Flight, self).__init__(**kwargs)
