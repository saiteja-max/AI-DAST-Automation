# agents/active_crawling_agent.py
import asyncio
from zapv2 import ZAPv2
from utils.ai_client import ai_analyze_text

class ActiveCrawlingAgent:
    def __init__(self, domain: str):
        self.domain = domain
        self.zap = ZAPv2(apikey="")

    async def run(self):
        print(f"[ActiveCrawlingAgent] Starting active crawling for {self.domain}")
        urls = await self.zap_spider(self.domain)
        enhanced = await ai_analyze_text(urls, prompt="Find URLs likely to have input forms or dynamic actions.")
        print(f"[ActiveCrawlingAgent] Crawled {len(urls)} URLs, AI marked {len(enhanced)} as interactive.")

    async def zap_spider(self, target):
        try:
            scan_id = self.zap.spider.scan(target)
            while int(self.zap.spider.status(scan_id)) < 100:
                await asyncio.sleep(2)
            return self.zap.spider.results(scan_id)
        except Exception as e:
            print(f"[ActiveCrawlingAgent] Error during ZAP spidering: {e}")
            return []
