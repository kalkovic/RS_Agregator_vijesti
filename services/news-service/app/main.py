from fastapi import FastAPI
from app.services.fetcher import AsyncRSSFetcher
from app.services.parser import RSSParser
from app.services.normalizer import ArticleNormalizer
from app.models.article import Article

app = FastAPI(title="News Aggregator - News Service")

RSS_SOURCES = {
    "index": "https://www.index.hr/rss",
    "jutarnji": "https://www.jutarnji.hr/rss",
    "24sata": "https://www.24sata.hr/feeds/najnovije.xml"
}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "news-service"}

@app.post("/api/fetch", response_model=list[Article])
async def fetch_and_normalize_news():
    """
    Pokreće ručni in-memory pipeline:
    1. Asinkrono dohvaća sirovi XML sa svih RSS izvora.
    2. Parsira XML u sirove rječnike.
    3. Normalizira podatke u Pydantic Article modele (generira ID, validira URL i datetime).
    """
    fetcher = AsyncRSSFetcher()
    
    raw_xml_data = await fetcher.fetch_all_feeds(RSS_SOURCES)
    
    all_normalized_articles = []
    
    for source_key, xml_content in raw_xml_data.items():
        raw_articles = RSSParser.parse_xml(xml_content)
        
        for raw_art in raw_articles:
            try:
                normalized_art = ArticleNormalizer.normalize_article(raw_art, source_key)
                all_normalized_articles.append(normalized_art)
            except Exception as e:
                continue
                
    return all_normalized_articles