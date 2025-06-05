import requests
import xml.etree.ElementTree as ET
import logging
from datetime import datetime
import email.utils

# Прямо хардкодим рабочий RSS
RSS_FEED_URL = "https://rus.lsm.lv/rss/"

def get_news_headlines(max_items=5):
    """Fetches the latest news headlines from the RSS feed, with a fallback to recent items."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.212 Safari/537.36"
        )
    }

    try:
        response = requests.get(RSS_FEED_URL, headers=headers, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        # Strip namespaces for simpler tag lookup
        for elem in root.iter():
            if isinstance(elem.tag, str) and '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]

        headlines = []
        today = datetime.now().date()

        # First, try to collect today's headlines
        for item in root.findall(".//item"):
            pub_date_text = item.findtext("pubDate") or ""
            try:
                pub_date = email.utils.parsedate_to_datetime(pub_date_text).date()
            except Exception:
                continue

            if pub_date == today:
                title = item.findtext("title") or ""
                description = item.findtext("description") or ""
                entry = f"- {title}\n  {description.strip()}"
                headlines.append(entry)
                if len(headlines) >= max_items:
                    break

        # Fallback to the most recent items if none from today
        if not headlines:
            for item in root.findall(".//item")[:max_items]:
                title = item.findtext("title") or ""
                description = item.findtext("description") or ""
                headlines.append(f"- {title}\n  {description.strip()}")

        return "\n".join(headlines) if headlines else "No news found."
    except Exception as e:
        logging.exception("Error fetching news")
        return f"Failed to fetch the latest news: {e}"

if __name__ == "__main__":
    print(" Checking if LSM news headlines are fetched...")
    print(" HEADLINES:\n", get_news_headlines())
