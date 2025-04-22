import uuid
from datetime import datetime

from sqlalchemy.dialects.mysql import JSON
from sqlalchemy_serializer import SerializerMixin

from app.ext.extensions import db


class InspectionRecord(db.Model, SerializerMixin):
    __tablename__ = 'inspection_records'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    inspection_id = db.Column(db.String(50), primary_key=True)
    inspection_name = db.Column(db.String(50))
    task_id = db.Column(db.String(50), db.ForeignKey('tasks.task_id', ondelete='CASCADE'), nullable=False,
                        comment='所属任务编号')
    executor_id = db.Column(db.String(50), db.ForeignKey('engineers.engineer_id', ondelete='SET NULL'),
                            comment='执行工程师')
    progress = db.Column(db.Integer, default=0, comment='完成百分比')
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    inspection_status = db.Column(db.String(50), db.ForeignKey('dictionary.dict_key'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)

    reference_image_id = db.Column(db.String(50),
                                   db.ForeignKey('aircraft_reference_image.image_id', ondelete='CASCADE'))
    # Relationships
    task = db.relationship('Task', backref='inspection_records')
    status_dict = db.relationship('Dictionary', foreign_keys=[inspection_status])
    items = db.relationship('InspectionItem', backref='inspection', lazy='dynamic')

    reference_image = db.relationship('AircraftReferenceImage', backref='inspection_records')

    def __init__(self, **kwargs):
        if 'inspection_id' not in kwargs:
            kwargs['inspection_id'] = str(uuid.uuid4())
        super(InspectionRecord, self).__init__(**kwargs)


class InspectionItem(db.Model, SerializerMixin):
    __tablename__ = 'inspection_item'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    item_id = db.Column(db.String(50), primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    inspection_id = db.Column(db.String(50), db.ForeignKey('inspection_records.inspection_id'))
    item_point = db.Column(JSON, comment='单个点位,送测照片,点位坐标+照片Json')
    description = db.Column(db.Text)
    result = db.Column(JSON, comment='检测结果')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.utcnow, nullable=False)
    model_id = db.Column(db.String(50), db.ForeignKey('models.model_id'), comment='使用的模型')
    model = db.relationship('Model', backref='inspection_item')

    # Relationships

    def __init__(self, **kwargs):
        if 'item_id' not in kwargs:
            kwargs['item_id'] = str(uuid.uuid4())
        super(InspectionItem, self).__init__(**kwargs)
