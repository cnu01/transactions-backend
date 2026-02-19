from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field

from app.constants import STATUS_PROCESSING


class Transaction(Document):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str
    status: str = Field(default=STATUS_PROCESSING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None
    
    class Settings:
        name = "transactions"
    
    class Settings:
        name = "transactions"
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "txn_abc123def456",
                "source_account": "acc_user_789",
                "destination_account": "acc_merchant_456",
                "amount": 1500,
                "currency": "INR",
                "status": "PROCESSING",
                "created_at": "2024-01-15T10:30:00Z",
                "processed_at": None
            }
        }
