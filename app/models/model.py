from app.ext.extensions import db
import uuid


class Model(db.Model):
    __tablename__ = 'models'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    model_id = db.Column(db.String(50), primary_key=True)
    model_name = db.Column(db.String(255))
    model_description = db.Column(db.Text)
    model_aircraft_type_id = db.Column(db.String(50))

    def __init__(self, **kwargs):
        if 'model_id' not in kwargs:
            kwargs['model_id'] = str(uuid.uuid4())
        super(Model, self).__init__(**kwargs)