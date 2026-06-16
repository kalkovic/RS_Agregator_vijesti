from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class Article(BaseModel):
    id: str
    title: str
    url: HttpUrl
    source: str
    category: str | None = None
    published_at: datetime
    event_id: str | None = None


class ArticleCreate(BaseModel):
    title: str
    url: HttpUrl
    source: str
    category: str | None = None
    published_at: datetime
