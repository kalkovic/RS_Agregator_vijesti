import asyncio
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncRSSFetcher:
    def __init__(self, timeouts: int = 10):
        self.timeout = aiohttp.ClientTimeout(total=timeouts)

    async def fetch_single_feed(self, session: aiohttp.ClientSession, source_name: str, url: str) -> str | None:
        """Dohvaća XML sadržaj za jedan RSS izvor."""
        try:
            logger.info(f"Pokrećem dohvaćanje za: {source_name} ({url})")
            async with session.get(url, timeout=self.timeout) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.error(f"Greška pri dohvaćanju {source_name}: Status {response.status}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout prilikom dohvaćanja feeda za: {source_name}")
            return None
        except Exception as e:
            logger.error(f"Neočekivana greška za {source_name}: {str(e)}")
            return None

    async def fetch_all_feeds(self, sources: dict[str, str]) -> dict[str, str]:
        """Paralelno dohvaća sve zadane RSS feedove."""
        async with aiohttp.ClientSession() as session:
            tasks = {
                source_name: self.fetch_single_feed(session, source_name, url)
                for source_name, url in sources.items()
            }
            
            results = await asyncio.gather(*tasks.values())
            
            return {
                source_name: result 
                for source_name, result in zip(tasks.keys(), results) 
                if result is not None
            }

if __name__ == "__main__":
    test_sources = {
        "index": "https://www.index.hr/rss",
        "jutarnji": "https://www.jutarnji.hr/rss",
        "24sata": "https://www.24sata.hr/feeds/najnovije.xml"
    }
    fetcher = AsyncRSSFetcher()
    asyncio.run(fetcher.fetch_all_feeds(test_sources))