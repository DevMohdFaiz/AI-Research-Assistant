import os
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_tavily import TavilySearch, tavily_search
from langchain_community.tools import tool
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Dict
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
                tailvy_result = self.tailvy_search.invoke({'query': query})
                for res in tailvy_result.get("results"):
                    sources.append({
                        "type": "tailvy_web",
                        "url": res.get("url"),
                        "title": res.get("title"),
                        "content": res.get("content"),
                        "score": res.get("score")
                    })
            except Exception as e:
                print(f"Web search error {e}")

        
        if search_type in ["wiki", "all"]:
            try:                
                wiki_response = self.wiki_search.invoke(query)
                sources.append({
                        "type": "wikipedia",
                        "url": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
                        "title": query,
                        "content": wiki_response,
                        "score": 1.0
                })
            except Exception as e:
                print(f"Wikipedia search error {e}")

        return sources
        
    
    def search(self, topic:str):
        """Search the web for sources using various queries"""
        topics  = self._generate_diverse_topics(topic)
        all_sources = {"topic": [], "sources": []}
        for topic in topics:
            all_sources["topic"].append(topic)
            all_sources["sources"].append(
                self.search_topic(topic)
            )


        unique_urls = set()
        for res in all_sources["sources"]:
            for source in res:
                url = source["url"]
                if url not in unique_urls:
                    unique_urls.add(url)

        return all_sources, unique_urls 
    

    def _generate_diverse_topics(self, topic:str, num_queries:int =5)-> List:
        """Generate different topics from the user topic"""

        class DiverseTopics(BaseModel):
            queries: List[str] = Field(description="A list of diverse topics generated")

        llm = ChatGroq(api_key=GROQ_API_KEY, temperature=0.6, model="llama-3.1-8b-instant").with_structured_output(DiverseTopics)
        prompt = ChatPromptTemplate.from_template("""
            You are an expert AI assistant at generating diverse topics from a given research topic
            Generate {num_queries} diverse search queries to research this topic comprehensively:

            Topic: {topic}

            Requirements:
            - Cover different aspects
            - Include specific and broad queries
            - Focus on credible sources
            - Aim for depth and breadth

            Return only the query var in a a JSON. 
            DO NOT APPEND ANYTHING ELSE TO THE JSON
            """)
        chain = prompt | llm 
        response = chain.invoke({"topic": topic, "num_queries": num_queries})

        return response.queries
    
