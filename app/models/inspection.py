from sqlalchemy_serializer import SerializerMixin

from app.ext.extensions import db
from datetime import datetime
import uuid
from sqlalchemy.dialects.mysql import JSON


class InspectionRecord(db.Model,SerializerMixin):
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
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(),onupdate=datetime.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)

    # Relationships
    task = db.relationship('Task', backref='inspection_records')
    status_dict = db.relationship('Dictionary', foreign_keys=[inspection_status])
    projects = db.relationship('InspectionProject', backref='inspection', lazy='dynamic')

    def __init__(self, **kwargs):
        if 'inspection_id' not in kwargs:
            kwargs['inspection_id'] = str(uuid.uuid4())
        super(InspectionRecord, self).__init__(**kwargs)


class InspectionProject(db.Model,SerializerMixin):
    __tablename__ = 'inspection_projects'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    project_id = db.Column(db.String(50), primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    inspection_id = db.Column(db.String(50), db.ForeignKey('inspection_records.inspection_id'))
    model_id = db.Column(db.String(50), db.ForeignKey('models.model_id'), comment='使用的模型')
    project_points = db.Column(JSON, comment='各个点位,检测结果,检测图url,json数据')
    description = db.Column(db.Text)
    reference_images = db.Column(JSON, comment='参考图片路径或URL的JSON数组')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.utcnow, nullable=False)

    # Relationships
    model = db.relationship('Model', backref='inspection_projects')

    def __init__(self, **kwargs):
        if 'project_id' not in kwargs:
            kwargs['project_id'] = str(uuid.uuid4())
        super(InspectionProject, self).__init__(**kwargs)