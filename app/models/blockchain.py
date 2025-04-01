from app.ext.extensions import db
from datetime import datetime
import uuid


class BlockchainTransaction(db.Model):
    __tablename__ = 'blockchain_transactions'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    transaction_id = db.Column(db.String(100), primary_key=True)
    inspection_id = db.Column(db.String(50), db.ForeignKey('inspection_records.inspection_id', ondelete='CASCADE'))
    transaction_hash = db.Column(db.String(255), nullable=False, comment='交易哈希')
    block_number = db.Column(db.BigInteger)
    transaction_data = db.Column(db.Text, comment='传递信息')
    timestamp = db.Column(db.DateTime)
    status = db.Column(db.String(50), db.ForeignKey('dictionary.dict_key'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now(),onupdate=datetime.now(), nullable=False)

    # Relationships
    inspection = db.relationship('InspectionRecord', backref='blockchain_transactions')
    status_dict = db.relationship('Dictionary', foreign_keys=[status])

    def __init__(self, **kwargs):
        if 'transaction_id' not in kwargs:
            kwargs['transaction_id'] = str(uuid.uuid4())
        super(BlockchainTransaction, self).__init__(**kwargs)