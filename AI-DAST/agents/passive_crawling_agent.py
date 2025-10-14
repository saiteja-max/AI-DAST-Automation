# agents/passive_crawling_agent.py
import aiohttp
from utils.ai_client import ai_analyze_text

class PassiveCrawlingAgent:
    def __init__(self, domain: str):
        self.domain = domain
        self.sources = [
            f"https://web.archive.org/cdx/search/cdx?url=*.{domain}&output=json&collapse=urlkey",
            f"https://urlscan.io/api/v1/search/?q=domain:{domain}"
        ]

    async def run(self):
        print(f"[PassiveCrawlingAgent] Passive crawling {self.domain}")
        urls = await self.fetch_urls()
        enriched = await ai_analyze_text(urls, prompt="Filter meaningful URLs and API endpoints for crawling.")
        print(f"[PassiveCrawlingAgent] Collected {len(urls)} URLs, AI filtered {len(enriched)} endpoints.")
        # Save or pass to active crawler

    async def fetch_urls(self):
        urls = []
        async with aiohttp.ClientSession() as session:
            for src in self.sources:
                try:
                    async with session.get(src, timeout=10) as resp:
                        if resp.status == 200:
                            data = await resp.text()
                            urls.append(data)
                except Exception as e:
                    print(f"[PassiveCrawlingAgent] Error fetching from {src}: {e}")
        return urls
