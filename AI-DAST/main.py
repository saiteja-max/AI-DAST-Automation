# main.py
import asyncio
from agents import ReconAgent

if __name__ == "__main__":
    domain = input("Enter target domain: ").strip()
    mode = input("Enter mode (all / enum / passive / active): ").strip()
    recon = ReconAgent(domain, mode)
    asyncio.run(recon.run())
