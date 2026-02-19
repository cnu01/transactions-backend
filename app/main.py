import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.config import settings
from app.constants import INDEX_TRANSACTION_ID
from app.models import Transaction
from app.routes import health, webhooks, transactions

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(settings.mongodb_url)
    database = client[settings.database_name]
    
    try:
        await init_beanie(database=database, document_models=[Transaction])
        await Transaction.get_pymongo_collection().create_index(
            "transaction_id", unique=True, name=INDEX_TRANSACTION_ID
        )
        logger.info(f"Connected to MongoDB: {settings.database_name}")
    except Exception as e:
        logger.error(f"DB init failed: {str(e)}")
        raise
    
    yield
    
    client.close()


app = FastAPI(
    title="Transaction Webhook Service",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(health.router)
app.include_router(webhooks.router)
app.include_router(transactions.router)
