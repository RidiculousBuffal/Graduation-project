from datetime import datetime

from sqlalchemy_serializer import SerializerMixin

from app.ext.extensions import db


class AuditLog(db.Model,SerializerMixin):
    __tablename__ = 'audit_logs'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    log_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id', ondelete='SET NULL'))
    action = db.Column(db.JSON, comment='详细操作')  # 存储操作详情，JSON格式，以便扩展
    blockchain_tx_hash = db.Column(db.String(66), nullable=True, comment='区块链交易哈希')  # 交易哈希，如0x...
    blockchain_block_number = db.Column(db.BigInteger, nullable=True, comment='区块链块高度')  # 交易所在区块号
    blockchain_operator = db.Column(db.String(42), nullable=True, comment='区块链操作者地址')  # 操作者地址，如0x...
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now(), onupdate=datetime.now(),nullable=False)

    def __repr__(self):
        return f"<AuditLog(log_id={self.log_id}, user_id={self.user_id}, action={self.action})>"