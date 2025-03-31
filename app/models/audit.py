from datetime import datetime

from app.ext.extensions import db


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    log_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id', ondelete='SET NULL'))
    action = db.Column(db.String(50), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)
    resource_id = db.Column(db.String(100))
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now(), onupdate=datetime.now(),nullable=False)
