# agents/subdomain_enum_agent.py
import asyncio
import aiohttp
from utils.ai_client import ai_analyze_text

class SubdomainEnumerationAgent:
    def __init__(self, domain: str):
        self.domain = domain
        self.sources = [
            f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names",
            f"https://crt.sh/?q={domain}&output=json",
            f"https://api.hackertarget.com/hostsearch/?q={domain}",
            f"https://urlscan.io/api/v1/search/?q=domain:{domain}",
            f"https://api.subdomain.center/?domain={domain}",
            f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/url_list?limit=500&page=1",
            f"https://dns.projectdiscovery.io/dns/{domain}/subdomains",
            f"https://web.archive.org/cdx/search/cdx?url=*.{domain}&output=json&collapse=urlkey"
        ]

    async def run(self):
        print(f"[SubdomainEnumerationAgent] Collecting subdomains for {self.domain}")
        subs = await self.fetch_subdomains()
        enhanced_subs = await ai_analyze_text(subs, prompt="Generate likely additional business-related subdomains.")
        print(f"[SubdomainEnumerationAgent] Found {len(subs)} + AI suggested {len(enhanced_subs)} subdomains.")
        # Save or return list

    async def fetch_subdomains(self):
        results = []
        async with aiohttp.ClientSession() as session:
            for url in self.sources:
                try:
                    async with session.get(url, timeout=10) as resp:
                        if resp.status == 200:
                            data = await resp.text()
                            results.append(data)
                except Exception as e:
                    print(f"[SubdomainEnumerationAgent] Error fetching from {url}: {e}")
        return results
