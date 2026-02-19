# Transaction Webhook Service

Handles payment transaction webhooks. Returns fast, processes in background.

## Quick Start

**Prerequisites:** Python 3.11+ and MongoDB running locally

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload --port 8000
```

Or just use `./run.sh`

Server runs at http://localhost:8000

## API

**Health Check**
```bash
curl http://localhost:8000/
```

**Send Webhook** (returns 202 immediately)
```bash
curl -X POST http://localhost:8000/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{"transaction_id":"txn_123","source_account":"acc_user_1","destination_account":"acc_merchant_1","amount":1500,"currency":"INR"}'
```

**Get Transaction**
```bash
curl http://localhost:8000/v1/transactions/txn_123
```

## Testing
```bash
# Send a webhook
curl -X POST http://localhost:8000/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{"transaction_id":"test_001","source_account":"acc1","destination_account":"acc2","amount":100,"currency":"INR"}'

# Check status right away
curl http://localhost:8000/v1/transactions/test_001

# Wait and check again
sleep 35 && curl http://localhost:8000/v1/transactions/test_001

# Send duplicate
curl -X POST http://localhost:8000/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{"transaction_id":"test_001","source_account":"acc1","destination_account":"acc2","amount":100,"currency":"INR"}'
```

## Tech Stack

**FastAPI** - Needed async support for background processing. The built-in async stuff and auto docs sealed the deal.

**MongoDB + Beanie** - Transaction data fits well in documents. Beanie makes async operations cleaner than raw motor.

**asyncio.create_task()** - Just using Python's native async tasks. 

**Idempotency** - Unique index on transaction_id in MongoDB. If duplicate comes in, DB throws DuplicateKeyError and we catch it.

## Project Structure

```
app/
├── routes/          
│   ├── health.py
│   ├── webhooks.py
│   └── transactions.py
├── services/
│   └── transaction_service.py
├── config.py
├── constants.py
├── main.py
├── models.py
└── schemas.py
```

## Config

Set these in `.env` if needed:
```bash
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=transaction_service
```

Defaults work fine for local dev.

## How It Works

Webhook hits the endpoint → returns 202 instantly (2-5ms) → transaction saved with PROCESSING status → background task waits 30s (simulating external API) → updates to PROCESSED.

Duplicate webhooks? Unique index on transaction_id catches them. Same 202 response, no duplicates in DB.

