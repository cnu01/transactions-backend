import logging
from datetime import datetime

from fastapi import APIRouter, status
from pymongo.errors import DuplicateKeyError

from app.constants import STATUS_PROCESSING, MSG_WEBHOOK_RECEIVED
from app.schemas import WebhookRequest, WebhookResponse
from app.models import Transaction
from app.services.transaction_service import process_transaction_background

router = APIRouter(prefix="/v1/webhooks", tags=["Webhooks"])
logger = logging.getLogger(__name__)


@router.post("/transactions", status_code=status.HTTP_202_ACCEPTED, response_model=WebhookResponse)
async def receive_webhook(webhook_data: WebhookRequest):
    try:
        transaction = Transaction(
            transaction_id=webhook_data.transaction_id,
            source_account=webhook_data.source_account,
            destination_account=webhook_data.destination_account,
            amount=webhook_data.amount,
            currency=webhook_data.currency,
            status=STATUS_PROCESSING,
            created_at=datetime.utcnow()
        )
        await transaction.insert()
        await process_transaction_background(webhook_data.transaction_id)
        
        logger.info(f"Webhook received: {webhook_data.transaction_id}")
        return WebhookResponse(
            message=MSG_WEBHOOK_RECEIVED,
            transaction_id=webhook_data.transaction_id
        )
    except DuplicateKeyError:
        logger.info(f"Duplicate webhook: {webhook_data.transaction_id}")
        return WebhookResponse(
            message=MSG_WEBHOOK_RECEIVED,
            transaction_id=webhook_data.transaction_id
        )
