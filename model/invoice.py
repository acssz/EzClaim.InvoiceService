from config.database import db

from .base import BaseModel

class Invoice(BaseModel):
    __tablename__ = "invoice"

    user_id = db.Column(db.String(36), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
        }
