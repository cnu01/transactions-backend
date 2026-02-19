from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.constants import MSG_WEBHOOK_RECEIVED


class WebhookRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    source_account: str = Field(..., min_length=1)
    destination_account: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    
    @field_validator('currency')
    @classmethod
    def currency_uppercase(cls, v: str) -> str:
        return v.upper()


class WebhookResponse(BaseModel):
    message: str = Field(default=MSG_WEBHOOK_RECEIVED)
    transaction_id: str


class TransactionResponse(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "txn_abc123def456",
                "source_account": "acc_user_789",
                "destination_account": "acc_merchant_456",
                "amount": 150.50,
                "currency": "INR",
                "status": "PROCESSED",
                "created_at": "2024-01-15T10:30:00Z",
                "processed_at": "2024-01-15T10:30:30Z"
            }
        }
