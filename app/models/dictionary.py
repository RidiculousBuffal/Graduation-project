import uuid
from datetime import datetime

from app.ext.extensions import db


class Dictionary(db.Model):
    __tablename__ = 'dictionary'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    dict_key = db.Column(db.String(50), primary_key=True)
    dict_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    parent_key = db.Column(db.String(50), db.ForeignKey('dictionary.dict_key', ondelete='SET NULL'))
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(),onupdate=datetime.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=datetime.now(), nullable=False)

    # Relationships
    children = db.relationship('Dictionary', backref=db.backref('parent', remote_side=[dict_key]))

    def __init__(self, **kwargs):
        if 'dict_key' not in kwargs:
            kwargs['dict_key'] = str(uuid.uuid4())
        super(Dictionary, self).__init__(**kwargs)
