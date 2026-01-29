import requests
from bs4 import BeautifulSoup
from typing import List
from tqdm import tqdm

class ContentExtractor:
    """Extract content from Internet webpages"""

    def __init__(self):
        self.headers = {"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}      

        
    def _extract_content(self, url):
        response = requests.get(url, headers=self.headers, timeout=100)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')

        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        title = soup.find("title")
        title.get_text().strip() if title else "Untitled"

        main_tags = [
            soup.find("main"),
            soup.find("article"),
            soup.find("div", class_="content"),
            soup.find("div", class_="main")
        ]

        for tag in main_tags:
            if tag:
                text = tag.get_text(separator="\n", strip=True)
                if len(text) > 250:
                    return text
                    
        body = soup.find("body")
        if body:
            return body.get_text(separator="\n", strip=True)
        
        return soup.get_text(separator="\n", strip=True)

    def extract_content(self, url):
        """Scrape webpage and extract main contents"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()        
            soup = BeautifulSoup(response.content, "lxml")

            for tag in soup(['style', 'header', 'footer', 'script', 'nav', 'aside', 'form']):
                tag.decompose()
                title = soup.find("title")
                title = title.get_text() if title else "Untitled"
                content = ""
                main_tags = [
                    soup.find("main"),
                    soup.find("article"),
                    soup.find("div", class_="content"),
                    soup.find("div", class_="main")
                ]
                found_main = False

                for tag in main_tags:
                    if tag:
                        text = tag.get_text(separator="\n", strip=True)
                        if len(text) > 250:
                            content = text
                            found_main = True
                            break
                if not found_main:
                    body = soup.find("body")
                    if body:
                        content = body.get_text(separator="\n", strip=True)
                    else:
                        content = soup.get_text(separator="\n", strip=True)


            return {
                    "url": url,
                    "title": title,
                    "content": content, 
                    "word_count": len(content.split())
            }
        
        except Exception as e:
            print(f"Error extracting from {url} => {e}")
            return None
        
    
    def extract_contents(self, urls:List[str]):
        """Extract contents from multiple urls"""
        all_contents= []
        for url in tqdm(urls, desc="Extracting contents..."):
            all_contents.append(
                self.extract_content(url)
            )
        return all_contents