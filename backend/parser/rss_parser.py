
import requests
import xml.etree.ElementTree as ET
from config.config import RSS_FEED_URL



class RssParser:
    def __init__(self, url=None):
        self.url = url or RSS_FEED_URL

    def get_headlines(self, limit=5) -> str:
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            headlines = [item.find('title').text for item in root.findall(".//item")[:limit]]
            return "\n".join(f"• {h}" for h in headlines) if headlines else "No news available."
        except Exception as e:
            print(f"⚠️ Error fetching news: {e}")
            return "Failed to fetch the latest news."


if __name__ == "__main__":
    parser = RssParser()
    headlines = parser.get_headlines()
    print("🔥 HEADLINES:\n", headlines)
