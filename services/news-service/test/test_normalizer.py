import pytest
from datetime import datetime
from app.services.parser import RSSParser
from app.services.normalizer import ArticleNormalizer

SAMPLE_RSS = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
    <channel>
        <item>
            <title>Testna vijest o blockchainu</title>
            <link>https://www.index.hr/vijesti/123</link>
            <pubDate>Thu, 18 Jun 2026 12:00:00 +0200</pubDate>
            <category>Tehnologija</category>
        </item>
    </channel>
</rss>
"""

def test_rss_parsing_and_normalization():
    raw_articles = RSSParser.parse_xml(SAMPLE_RSS)
    assert len(raw_articles) == 1
    assert raw_articles[0]["title"] == "Testna vijest o blockchainu"

    normalized = ArticleNormalizer.normalize_article(raw_articles[0], "index")
    
    assert normalized.id != ""
    assert normalized.source == "index-hr"
    assert isinstance(normalized.published_at, datetime)
    assert normalized.published_at.year == 2026