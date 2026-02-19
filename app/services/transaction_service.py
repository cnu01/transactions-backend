import asyncio
import logging
from datetime import datetime

from app.constants import STATUS_PROCESSED, STATUS_PROCESSING, PROCESSING_DELAY_SECONDS
from app.models import Transaction

logger = logging.getLogger(__name__)


async def process_transaction_background(transaction_id: str):
    asyncio.create_task(_process_transaction(transaction_id))


async def _process_transaction(transaction_id: str):
    try:
        transaction = await Transaction.find_one(
            Transaction.transaction_id == transaction_id
        )
        
        if not transaction:
            logger.warning(f"Transaction not found: {transaction_id}")
            return
        
        if transaction.status == STATUS_PROCESSED:
            logger.info(f"Already processed: {transaction_id}")
            return
        
        logger.info(f"Processing: {transaction_id}")
        await asyncio.sleep(PROCESSING_DELAY_SECONDS)
        
        transaction.status = STATUS_PROCESSED
        transaction.processed_at = datetime.utcnow()
        await transaction.save()
        
        logger.info(f"Processed: {transaction_id}")
    except Exception as e:
        logger.error(f"Error processing {transaction_id}: {str(e)}", exc_info=True)
