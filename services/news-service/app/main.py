import logging

from fastapi import FastAPI

from app.config import settings

logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))

app = FastAPI(
    title="News Service",
    description="RSS aggregation, event grouping, and blockchain integrity verification",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "news-service"}
