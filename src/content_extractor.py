import requests
from bs4 import BeautifulSoup


class ContentExtractor:
    """Extract content from Internet webpages"""

    def __init__(self):
        self.headers = {"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    def get_web_content(self, url:str):
        response = requests.get(url, headers=self.headers, timeout=150)
        response.raise_for_status()
        soup = BeautifulSoup(response.context, "lxml")

        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        title = soup.get('title')
        title = title if title else "Untitled"

        main_tags = [
            soup.find('main'), soup.find('article'), soup.find('div', class_='content'), soup.find('div', class_='main')
        ]
        for tag in main_tags:
            if tag:
                text = tag.get_text(separator="\n", strip=True)
                
