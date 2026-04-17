"""
Web tools — search, fetch pages, and global news briefings.
"""

import httpx
import xml.etree.ElementTree as ET
import asyncio  # Required for parallel execution
import re
from datetime import datetime

SEED_FEEDS = [
    'https://feeds.bbci.co.uk/news/world/rss.xml',
    'https://www.cnbc.com/id/100727362/device/rss/rss.html',
    'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    'https://www.aljazeera.com/xml/rss/all.xml'
]

async def fetch_and_parse_feed(client, url):
    """Helper function to handle a single feed request and parse its XML."""
    try:
        response = await client.get(url, headers={'User-Agent': 'Friday-AI/1.0'}, timeout=5.0)
        if response.status_code != 200:
            return []

        root = ET.fromstring(response.content)
        # Extract source name from URL (e.g., 'BBC' or 'NYTIMES')
        source_name = url.split('.')[1].upper()
        
        feed_items = []
        # Get top 5 items per feed
        items = root.findall(".//item")[:5]
        for item in items:
            title = item.findtext("title")
            description = item.findtext("description")
            link = item.findtext("link")
            
            if description:
                description = re.sub('<[^<]+?>', '', description).strip()

            feed_items.append({
                "source": source_name,
                "title": title,
                "summary": description[:200] + "..." if description else "",
                "link": link
            })
        return feed_items
    except Exception:
        # If one feed fails, return an empty list so others can still succeed
        return []

async def get_world_news(**kwargs) -> str:
    """
    Fetches the latest global headlines from major news outlets simultaneously.
    Use this when the user asks 'What's going on in the world?' or for recent events.
    """
    async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
        tasks = [fetch_and_parse_feed(client, url) for url in SEED_FEEDS]
        results_of_lists = await asyncio.gather(*tasks)
        all_articles = [item for sublist in results_of_lists for item in sublist]

    if not all_articles:
        return "The global news grid is unresponsive, sir. I'm unable to pull headlines."

    report = ["### GLOBAL NEWS BRIEFING (LIVE)\n"]
    for entry in all_articles[:12]:
        report.append(f"**[{entry['source']}]** {entry['title']}")
        report.append(f"{entry['summary']}")
        report.append(f"Link: {entry['link']}\n")

    return "\n".join(report)

async def search_web(query: str, **kwargs) -> str:
    """Search the web for a given query and return a summary of results."""
    # Note: duckduckgo_search integration can be added here
    return f"[stub] Search results for: {query}"

async def fetch_url(url: str, **kwargs) -> str:
    """Fetch the raw text content of a URL."""
    async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text[:4000]

async def open_world_monitor(**kwargs) -> str:
    """
    Opens the World Monitor dashboard (worldmonitor.app) in the system's web browser.
    Use this when the user wants a visual overview of global events or a real-time map.
    """
    import webbrowser
    url = "https://worldmonitor.app/"
    try:
        webbrowser.open(url)
        return "Displaying the World Monitor on your primary screen now, sir."
    except Exception as e:
        return f"I'm unable to initialize the visual monitor: {str(e)}"

def register(mcp):
    mcp.tool()(get_world_news)
    mcp.tool()(search_web)
    mcp.tool()(fetch_url)
    mcp.tool()(open_world_monitor)