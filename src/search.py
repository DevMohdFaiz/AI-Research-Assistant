import os
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_tavily import TavilySearch, tavily_search
from langchain_community.tools import tool
from config import TAVILY_API_KEY, GROQ_API_KEY

class SearchAgent:
    "Make web searches based on the user topic"

    def __init__(self):
        self.tailvy_search = TavilySearch(
            tavily_api_key=TAVILY_API_KEY, search_depth="advanced", max_resuslts=5, include_answer=True
        )
        self.wiki_search = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=5))

    
    def search_topic(self, query:str, search_type:str ="all"):
        """Search the user topic on the web or wikipedia"""

        sources = []
        if search_type in ["web", "all"]:
            try:                
                tailvy_result = tavily_search.invoke({'query': query})
                for res in tailvy_result.get("results"):
                    sources.append({
                        "type": "tailvy_web",
                        "url": res.get("url"),
                        "title": res.get("title"),
                        "content": res.get("content"),
                        "score": res.get("score")
                    })
            except Exception as e:
                print("Web search error {e}")

        
        if search_type in ["wiki", "all"]:
            try:                
                wiki_response = self.wiki.invoke("Kamala harris")
                sources.append({
                        "type": "wikipedia",
                        "url": f"https://en.wikipedia.org/wiki/{query.replace(" ", "_")}",
                        "title": query,
                        "content": wiki_response,
                        "score": 1.0
                })
            except Exception as e:
                print(f"Wikipedia search error {e}")
        