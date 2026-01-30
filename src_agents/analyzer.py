import time
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import GROQ_API_KEY, GROQ_API_KEY_2

class AnalyzerAgent:
    """Analyze sources"""

    def __init__(self, model="openai/gpt-oss-120b"):
        self.llm = ChatGroq(api_key=GROQ_API_KEY_2, model=model, temperature=0.1)

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

        content = source.get('content')[:]
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
            print(f"error: {e}")
            return None 
    
    def analyze_sources(self, sources, research_questions):
        """Analyze multiple sources and obtain key findings"""
        key_findings= []
        for source in sources:
            try:
                finding = self._analyze_source(source, research_questions)
                if finding:
                    key_findings.append(finding)
                    time.sleep(10)
            except Exception as e:
                print(f"Error: {e}")
        parsed_findings = self._parse_key_findings(key_findings)
        return key_findings, parsed_findings



    def analyze_sources_in_parallel(self, sources, research_questions:List):
        """Concurrently analyze multiple sources and obtain key findings"""
        key_findings = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_source = {
                executor.submit(
                    self._analyze_source, source, research_questions): source for source in sources
            }

        for _, future in enumerate(as_completed(future_to_source), 1):
            try:
                finding = future.result(timeout=50)
                if finding:
                    key_findings.append(finding)
            except Exception as e:
                print(f"error {e}")
                # return None

        parsed_findings = self._parse_key_findings(key_findings)
        return key_findings, parsed_findings
    
    def _parse_key_findings(self, key_findings):
        """Obtain the key findings from our sources and put them in a llm-friendly format"""
        parsed_findings = ""
        for _, analysis in enumerate(key_findings):
            parsed_findings += f"<h3>Title: {analysis.get('title')}</h3>"
            parsed_findings += f"<h4>Key Findings</h4> {analysis.get('key_points')}<hr>"