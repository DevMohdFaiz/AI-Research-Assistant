from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

class AnalyzerAgent:
    """Analyze sources"""

    def __init__(self):
        self.llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile", temperature=0.1)

    def _analyze_source(self, source, research_questions):
        """Read and analyze a single source"""
        prompt = ChatPromptTemplate.from_template("""
            You are an expert Research Assistant with great skill at extracting relevant information from given sources
            Analyze this source and extract key information relevant to the research questions 
            
            **Source**: {title}
                                                    
            Content:
            {content}
                                                    
            **Research Questions**
            {research_questions}
                
            Extract:
            1. Main points relevant to the research questions
            2. Key facts, statistics, or quotes
            3. Important insights or arguments

            Be concise. Focus only on information relevant to the research questions.

            Format as:
            - Point 1
            - Point 2
            - Point 3
            (etc.)                                                
        """)

        content = source.get('content')
        title = source.get('title')

        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "title": title, "content": content, "research_questions": research_questions
            })
            
            return {
                "title": title,
                "url": source.get("url"),
                "key_points": response.content
            }
        
        except Exception as e:
            return {"error": e}
    

    def analyze_sources(self, sources, research_questions:List):
        """Analyze multiple sources and obtain key findings"""
        final_findings = {}
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_source = {
                executor.submit(
                    self._analyze_source, source, research_questions): source for source in sources
            }

        for idx, future in enumerate(as_completed(future_to_source), 1):
            try:
                finding = future.result(timeout=50)
                if finding:
                    final_findings[idx] = finding
            except Exception as e:
                final_findings[idx] = f"error {e}"   

        return final_findings