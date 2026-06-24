import email.utils
import hashlib
from datetime import datetime, timezone
from app.models.article import Article

class ArticleNormalizer:
    @staticmethod
    def parse_to_datetime(raw_date: str) -> datetime:
        try:
            if not raw_date:
                return datetime.now(timezone.utc)
            return email.utils.parsedate_to_datetime(raw_date)
        except Exception:
            return datetime.now(timezone.utc)

    @classmethod
    def normalize_article(cls, raw_data: dict[str, str], source_key: str) -> Article:
        url_string = raw_data.get("link", "").strip()
        
        article_id = hashlib.md5(url_string.encode("utf-8")).hexdigest() if url_string else "unknown"

        return Article(
            id=article_id,
            title=raw_data.get("title", "").strip(),
            url=url_string,  
            source=f"{source_key}-hr",
            category=raw_data.get("category", "Općenito"),
            published_at=cls.parse_to_datetime(raw_data.get("pubDate", ""))
        )