# agents/recon_agent.py
import asyncio
from .subdomain_enum_agent import SubdomainEnumerationAgent
from .passive_crawling_agent import PassiveCrawlingAgent
from .active_crawling_agent import ActiveCrawlingAgent

class ReconAgent:
    def __init__(self, domain: str, mode: str = "all"):
        self.domain = domain
        self.mode = mode.lower()
        self.sub_enum_agent = SubdomainEnumerationAgent(domain)
        self.passive_agent = PassiveCrawlingAgent(domain)
        self.active_agent = ActiveCrawlingAgent(domain)

    async def run(self):
        print(f"[ReconAgent] Starting reconnaissance for: {self.domain} (mode={self.mode})")

        if self.mode == "all":
            await self.run_all()
        elif self.mode == "active":
            await self.active_agent.run()
        elif self.mode == "passive":
            await self.passive_agent.run()
        elif self.mode == "enum":
            await self.sub_enum_agent.run()
        else:
            print(f"[ReconAgent] Invalid mode '{self.mode}' — available modes: all, enum, passive, active")

    async def run_all(self):
        # Run all agents concurrently for speed
        await asyncio.gather(
            self.sub_enum_agent.run(),
            self.passive_agent.run(),
            self.active_agent.run()
        )

        print(f"[ReconAgent] Recon complete for {self.domain}.")
