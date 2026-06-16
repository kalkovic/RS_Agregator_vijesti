from datetime import datetime

from pydantic import BaseModel, Field

from app.models.article import Article


class Event(BaseModel):
    id: str
    title: str
    category: str | None = None
    articles: list[Article] = Field(default_factory=list)
    source_count: int = 0
    created_at: datetime
    updated_at: datetime
    content_hash: str | None = None
    blockchain_tx_hash: str | None = None
