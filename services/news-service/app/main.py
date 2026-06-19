from app.blockchain_utils import record_event_on_blockchain
from fastapi import FastAPI, Query, HTTPException
from app.services.fetcher import AsyncRSSFetcher
from app.services.parser import RSSParser
from app.services.normalizer import ArticleNormalizer
from app.models.article import Article
from app.models.event import Event  

from app.config import settings
from app.db.repository import get_all_active_events, save_events_and_articles, get_event_by_id
from app.services.aggregator import EventAggregator

app = FastAPI(title="News Aggregator - News Service")

RSS_SOURCES = {
    "index": "https://www.index.hr/rss",
    "jutarnji": "https://www.jutarnji.hr/rss",
    "24sata": "https://www.24sata.hr/feeds/najnovije.xml"
}

async def run_core_pipeline():

    print("\n--- [Pipeline] Pokrećem News Pipeline ---")
    
    print("[Pipeline] Dohvaćam postojeće događaje iz DynamoDB-a...")
    existing_events = get_all_active_events()
    print(f"[Pipeline] Nađeno postojećih događaja u bazi: {len(existing_events)}")

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
                
    print(f"[Pipeline] Uspješno normalizirano {len(all_normalized_articles)} članaka.")

    if not all_normalized_articles:
        print("[Pipeline] Nema novih članaka za obradu.")
        return []

    print("[Pipeline] Pokrećem Jaccard tekstualnu analizu i grupiranje...")
    aggregator = EventAggregator(similarity_threshold=settings.similarity_threshold)
    updated_articles, updated_events = aggregator.aggregate_articles(
        incoming_articles=all_normalized_articles, 
        existing_events=existing_events
    )

    print("[Pipeline] Zapisujem grupirane događaje i artikle u DynamoDB...")
    save_events_and_articles(updated_articles, updated_events)
    
    print("[Pipeline] Šaljem događaje na ovjeru na Blockchain...")
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
        
        blockchain_success = record_event_on_blockchain(event_id=event_id, articles=articles_list)
        if blockchain_success:
            print(f"🔗 Blockchain ovjera uspješna za event {event_id}.")
        else:
            print(f"⚠️ DynamoDB spremljen, ali zapis na blockchain nije uspio za {event_id}.")

    print("--- [Pipeline] Pipeline uspješno izvršen! ---\n")
    
    return updated_articles    


@app.on_event("startup")
async def startup_pipeline_task():

    try:
        await run_core_pipeline()
    except Exception as e:
        print(f"❌ [STARTUP ERROR] Automatski pipeline je pukao: {e}")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "news-service"}


@app.post("/api/fetch", response_model=list[Article])
async def fetch_and_normalize_news():
 
    articles = await run_core_pipeline()
    return articles

@app.get("/api/events", response_model=list[Event])
def get_all_events(
    q: str | None = Query(None, description="Pretraga po naslovu događaja"),
    category: str | None = Query(None, description="Filtriranje po kategoriji"),
    source: str | None = Query(None, description="Filtriranje po izvoru (npr. index-hr)")
):

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
 
    event = get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Događaj nije pronađen")
    return event