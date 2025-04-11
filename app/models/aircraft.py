import uuid

from sqlalchemy_serializer import SerializerMixin

from app.ext.extensions import db


class AircraftType(db.Model, SerializerMixin):
    __tablename__ = 'aircraft_type'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }

    typeid = db.Column(db.String(50), primary_key=True)
    type_name = db.Column(db.String(255), comment='飞机型号名')
    description = db.Column(db.Text, comment='描述')

    # Relationships
    aircrafts = db.relationship('Aircraft', backref='type', lazy='dynamic')

    serialize_rules = ('-aircrafts')

    def __init__(self, **kwargs):
        if 'typeid' not in kwargs:
            kwargs['typeid'] = str(uuid.uuid4())
        super(AircraftType, self).__init__(**kwargs)


class Aircraft(db.Model, SerializerMixin):
    __tablename__ = 'aircraft'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    aircraft_id = db.Column(db.String(50), primary_key=True)
    aircraft_name = db.Column(db.String(255), comment='飞机名字')
    age = db.Column(db.BigInteger)
    typeid = db.Column(db.String(50), db.ForeignKey('aircraft_type.typeid'), comment='飞机型号ID')

    # Relationships
    flights = db.relationship('Flight', backref='aircraft', lazy='dynamic')

    def __init__(self, **kwargs):
        if 'aircraft_id' not in kwargs:
            kwargs['aircraft_id'] = str(uuid.uuid4())
        super(Aircraft, self).__init__(**kwargs)


class AircraftReferenceImage(db.Model, SerializerMixin):
    __tablename__ = 'aircraft_reference_image'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }

    # 字段定义，与 SQL 表结构对应
    image_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='图片ID')
    image_name = db.Column(db.String(255), comment='图片名')
    image_description = db.Column(db.Text, comment='图片描述')
    image_json = db.Column(db.Text, comment='图片json格式点位')
    aircraft_id = db.Column(db.String(50), db.ForeignKey('aircraft.aircraft_id'), comment='飞机ID')

    # Relationships
    aircraft = db.relationship('Aircraft', backref='reference_images', lazy='joined')

    def __init__(self, **kwargs):
        super(AircraftReferenceImage, self).__init__(**kwargs)
