import logging
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.schemas import TransactionResponse
from app.models import Transaction

router = APIRouter(prefix="/v1/transactions", tags=["Transactions"])
logger = logging.getLogger(__name__)


@router.get("/{transaction_id}", response_model=List[TransactionResponse])
async def get_transaction(transaction_id: str):
    transaction = await Transaction.find_one(
        Transaction.transaction_id == transaction_id
    )
    
    if not transaction:
        logger.warning(f"Transaction not found: {transaction_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction {transaction_id} not found"
        )
    
    return [TransactionResponse(
        transaction_id=transaction.transaction_id,
        source_account=transaction.source_account,
        destination_account=transaction.destination_account,
        amount=transaction.amount,
        currency=transaction.currency,
        status=transaction.status,
        created_at=transaction.created_at,
        processed_at=transaction.processed_at
    )]
