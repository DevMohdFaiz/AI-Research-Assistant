import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time

class AsyncScraper:
    def __init__(self):
        # These headers mimic a real Chrome browser to bypass simple 403 blocks
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }

    async def fetch(self, session, url):
        """Async fetch with aggressive timeout"""
        try:
            async with session.get(url, headers=self.headers, timeout=10) as response:
                if response.status == 403:
                    return {"url": url, "error": "403 Forbidden (Blocked)"}
                
                response.raise_for_status()
                text = await response.text()
                return {"url": url, "html": text, "error": None}
        except Exception as e:
            return {"url": url, "error": str(e)}

    def parse(self, html_data):
        """Parse response and extract main contents from relevant tags"""
        if html_data.get("error"):
            return None

        try:
            soup = BeautifulSoup(html_data["html"], "lxml")
            for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "iframe", "ads"]):
                tag.decompose()

            title = soup.title.string.strip() if soup.title else "Untitled"
            content = ""
            main_tags = [
                soup.find("main"), soup.find("article"), 
                soup.find("div", class_="content"), soup.find("div", class_="main")
            ]
            
            for tag in main_tags:
                if tag:
                    text = tag.get_text(separator="\n", strip=True)
                    if len(text) > 250:
                        content = text
                        break
            
            if not content:
                body = soup.find("body")
                content = body.get_text(separator="\n", strip=True) if body else ""

            return {
                "url": html_data["url"],
                "title": title,
                "content": content,
                "word_count": len(content.split())
            }
        except Exception:
            return None

    async def scrape_urls(self, urls):
        """Main entry point"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in urls]
            raw_responses = await asyncio.gather(*tasks)

            results = []
            for resp in raw_responses:
                parsed = self.parse(resp)
                if parsed:
                    results.append(parsed)
                else:
                    if resp.get("error"):
                         print(f"Failed: {resp['url']} -> {resp['error']}")
            
            return results

