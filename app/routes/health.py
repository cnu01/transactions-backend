from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.utcnow().isoformat() + "Z"
    }
