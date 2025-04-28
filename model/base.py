import uuid
from config.database import db

class BaseModel(db.Model):
    __abstract__ = True  # 这表示 SQLAlchemy 不会给 BaseModel 创建表

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    def to_dict(self):
        raise NotImplementedError("You must implement to_dict method in subclass.")
