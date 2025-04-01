from app.ext.extensions import db
import uuid


class Terminal(db.Model):
    __tablename__ = 'terminal'
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    terminal_id = db.Column(db.String(50), primary_key=True)
    terminal_name = db.Column(db.String(50))
    description = db.Column(db.Text)

    def __init__(self, **kwargs):
        if 'terminal_id' not in kwargs:
            kwargs['terminal_id'] = str(uuid.uuid4())
        super(Terminal, self).__init__(**kwargs)