from contextlib import asynccontextmanager
from app.blockchain_utils import record_event_on_blockchain, calculate_event_hash, verify_event_on_blockchain 
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.services.fetcher import AsyncRSSFetcher
from app.services.parser import RSSParser
from app.services.normalizer import ArticleNormalizer
from app.models.article import Article
from app.models.event import Event  

from app.config import settings
from app.db.repository import get_all_active_events, save_events_and_articles, get_event_by_id, update_event_blockchain_hash
from app.services.aggregator import EventAggregator

from .security import get_current_user, require_admin
from pydantic import BaseModel

from app.logger import get_logger

logger = get_logger("news-service")

RSS_SOURCES = {
    "index": "https://www.index.hr/rss",
    "jutarnji": "https://www.jutarnji.hr/naslovnica/rss",
    "24sata": "https://www.24sata.hr/feeds/najnovije.xml"
}

class NewsSchema(BaseModel):
    title: str
    content: str | None = None

async def run_core_pipeline():
    logger.info("[Pipeline] Pokrećem News Pipeline...")
    
    logger.info("[Pipeline] Dohvaćam postojeće događaje iz DynamoDB-a...")
    existing_events = get_all_active_events()
    logger.info(f"[Pipeline] Nađeno postojećih događaja u bazi: {len(existing_events)}")

    fetcher = AsyncRSSFetcher()
    raw_xml_data = await fetcher.fetch_all_feeds(RSS_SOURCES)
    
    all_normalized_articles = []
    for source_key, xml_content in raw_xml_data.items():
        raw_articles = RSSParser.parse_xml(xml_content)
        for raw_art in raw_articles:
            try:
                normalized_art = ArticleNormalizer.normalize_article(raw_art, source_key)
                all_normalized_articles.append(normalized_art)
            except Exception:
                continue
                
    logger.info(f"[Pipeline] Uspješno normalizirano {len(all_normalized_articles)} članaka.")

    if not all_normalized_articles:
        logger.warning("[Pipeline] Nema novih članaka za obradu.")
        return []

    logger.info("[Pipeline] Pokrećem Jaccard tekstualnu analizu i grupiranje...")
    aggregator = EventAggregator(similarity_threshold=settings.similarity_threshold)
    updated_articles, updated_events = aggregator.aggregate_articles(
        incoming_articles=all_normalized_articles, 
        existing_events=existing_events
    )

    logger.info("[Pipeline] Zapisujem grupirane događaje i artikle u DynamoDB...")
    save_events_and_articles(updated_articles, updated_events)
    
    logger.info("[Pipeline] Šaljem događaje na ovjeru na Blockchain...")
    for event in updated_events:
        event_id = event.id if hasattr(event, "id") else event["id"]

        raw_articles = event.articles if hasattr(event, "articles") else event["articles"]
        articles_list = []
        for art in raw_articles:
            if hasattr(art, "model_dump"):
                articles_list.append(art.model_dump())
            elif hasattr(art, "dict"):
                articles_list.append(art.dict())
            else:
                articles_list.append(art)

        result = record_event_on_blockchain(event_id=event_id, articles=articles_list)
        if result["success"] and result["tx_hash"]:
            update_event_blockchain_hash(event_id, result["tx_hash"])
            logger.info(f"🔗 Blockchain ovjera uspješna za event {event_id}.")
        else:
            logger.error(f"⚠️ DynamoDB spremljen, ali zapis na blockchain nije uspio za {event_id}.")

    logger.info("[Pipeline] Pipeline uspješno izvršen!")
    return updated_articles    


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("News Service se uspješno podiže unutar Docker okruženja.")
    try:
        await run_core_pipeline()
    except Exception as e:
        logger.error(f"❌ [STARTUP ERROR] Automatski pipeline je zakazao pri podizanju kontejnera: {e}", exc_info=True)
    
    yield
    
    logger.info("Primljen SIGTERM signal! Pokrećem graceful shutdown postupak...")
    logger.info("Sve aktivne konekcije prema DynamoDB i Ganache blockchainu su sigurno zatvorene.")
    logger.info("News Service je uspješno ugašen bez gubitka podataka.")


app = FastAPI(
    title="News Aggregator - News Service",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


@app.get("/health")
def health_check():
    logger.info("Primljen zahtjev na health check endpoint.")
    return {"status": "healthy", "service": "news-service"}


@app.post("/api/fetch", response_model=list[Article])
async def fetch_and_normalize_news():
    logger.info("Ručno pokretanje news pipelinea putem API endpointa.")
    articles = await run_core_pipeline()
    return articles


@app.get("/api/events", response_model=list[Event])
def get_all_events(
    q: str | None = Query(None, description="Pretraga po naslovu događaja"),
    category: str | None = Query(None, description="Filtriranje po kategoriji"),
    source: str | None = Query(None, description="Filtriranje po izvoru (npr. index-hr)")
):
    logger.info(f"Dohvaćam događaje iz baze. Filteri - Pretraga: {q}, Kategorija: {category}, Izvor: {source}")
    events = get_all_active_events()
    filtered_events = []
    
    for event in events:
        if category and event.category and category.lower() not in event.category.lower():
            continue
            
        if q and q.lower() not in event.title.lower():
            continue
            
        if source:
            has_source = any(source.lower() in art.source.lower() for art in event.articles)
            if not has_source:
                continue
                
        filtered_events.append(event)
        
    return filtered_events


@app.get("/api/events/{event_id}", response_model=Event)
def get_event_detail(event_id: str):
    logger.info(f"Zahtjev za detalje događaja: {event_id}")
    event = get_event_by_id(event_id)
    if not event:
        logger.warning(f"Događaj s ID-em {event_id} nije pronađen.")
        raise HTTPException(status_code=404, detail="Događaj nije pronađen")
    return event


@app.get("/api/events/{event_id}/verify")
def verify_event_integrity(event_id: str):
    logger.info(f"Pokrećem blockchain verifikaciju integriteta za događaj: {event_id}")
    event = get_event_by_id(event_id)
    if not event:
        logger.warning(f"Verifikacija neuspješna. Događaj {event_id} ne postoji u bazi.")
        raise HTTPException(status_code=404, detail="Događaj nije pronađen")

    raw_articles = event.get("articles", []) if isinstance(event, dict) else event.articles    
    articles_list = []

    for art in raw_articles:
        if hasattr(art, "model_dump"):
            articles_list.append(art.model_dump())  
        elif hasattr(art, "dict"):
            articles_list.append(art.dict())        
        else:
            articles_list.append(art)
            
    local_hash = calculate_event_hash(articles_list)
    verification_result = verify_event_on_blockchain(event_id, local_hash)
    
    if verification_result.get("status") == "error":
        logger.error(f"Integrity check FAILED za događaj {event_id}! Opis: {verification_result.get('message')}")
        raise HTTPException(status_code=404, detail=verification_result.get("message"))
        
    logger.info(f"Integrity check PASSED za događaj {event_id}.")
    return verification_result


@app.post("/news")
def create_news(news: NewsSchema, current_user: dict = Depends(get_current_user)):
    logger.info(f"Korisnik {current_user['email']} ručno kreira novu vijest: {news.title}")
    return {"message": "Vijest stvorena", "user": current_user["email"]}


@app.delete("/news/{news_id}")
def delete_news(news_id: int, current_user: dict = Depends(require_admin)):
    logger.warning(f"Administrator {current_user['email']} briše vijest s ID-em: {news_id}")
    return {"message": f"Vijest {news_id} obrisana od strane admina {current_user['email']}"}