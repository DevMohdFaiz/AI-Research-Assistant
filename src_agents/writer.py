import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from tqdm import tqdm
from config import GROQ_API_KEY_2, GROQ_API_KEY


class WriterAgent:
    """Write the full paper section-wise"""

    def __init__(self, model="openai/gpt-oss-120b"):
        self.llm = ChatGroq(api_key= GROQ_API_KEY, model=model, temperature=0.1)

    
    def write_sections(self, sections, key_concepts, key_findings):
        full_paper_sections = {}
        for idx, section in tqdm(enumerate(sections), desc="Wrtting sections...", total=len(sections)):
            if section.lower() not in ["introduction", "conclusion"]:
                full_paper_sections[section] = self._write_section(section, key_concepts, key_findings)
                time.sleep(2)
        return full_paper_sections


    def _write_section(self, section, key_concepts, key_findings):
        prompt = ChatPromptTemplate.from_template("""
            You are an expert academic scholar who specializes in writing papers section-wise 
            The paper is to be written in different sections and then combined to form a full paper.                                          
            You are a single specific section ONLY!
            Strictly write the **{section}** section of this paper only. This is highly important!
            
            Note: Skip the **Introduction** and **Conclusion** sections. Those will be written later on

            Key Findings extracted various sources:
            {key_findings}
                                                
            Ensure that these concepts are fully explored:
            {key_concepts}
            
            Write a well-structured, academic section that:
            1. Presents information clearly and logically for each section you working on
            2. Synthesizes information from multiple sources
            3. Maintains an objective, scholarly tone
            4. Is approximately 300-500 words
            5. Includes proper transitions between ideas
            6. Properly cite sources from the given sources
            7. Strictly keep your writing based on the given sources
            9. Use inline citation where applicable
                                

            Write the section content (no title needed):
        """)
        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "section": section,
                "key_concepts": key_concepts,
                "key_findings": key_findings
            })
            return response.content

        except Exception as e:
            print(f"Error: {e}")
            return None
        


    from typing import List, Dict

    def write_introduction(self, topic: str, key_concepts, paper_outline) -> str:
        """Write introduction section."""
        
        prompt = ChatPromptTemplate.from_template("""
        Write an introduction for a research paper on this topic:

        **Topic:** {topic}
        **Key Concepts**: {key_concepts}

        **Paper Outline:**
        {outline}

        Write a compelling introduction (250-400 words) that:
        1. Introduces the topic and its importance
        2. Provides necessary background
        3. States what the paper will cover
        4. Engages the reader

        Write the introduction:
        """)
            
        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "topic":topic,
                "key_concepts": key_concepts,
                "outline": paper_outline
            })
            
            return response.content
            
        except Exception as e:
            print(f"Introduction writing error: {e}")
            return f"# Introduction\n\nThis paper explores {topic}."
        

        
    def write_conclusion(self, topic: str, summary, sections: Dict[str, str]) -> str:
        """Write conclusion section."""
        
        llm = ChatGroq(api_key= GROQ_API_KEY_2, model="llama-3.3-70b-versatile", temperature=0)
        prompt = ChatPromptTemplate.from_template("""
            Write a conclusion for this research paper.

            **Topic:** {topic}  

            **Paper Content Summary:**
            {summary}

            Write a strong conclusion (200-350 words) that:
            1. Summarizes key findings
            2. Synthesizes main insights
            3. Discusses implications
            4. Suggests future directions

            Write the conclusion:
        """)
        chain = prompt | llm
        try:
            response = chain.invoke({
                "topic": topic, "summary": summary, "sections": sections
            })
            return response.content
        
        except Exception as e:
            print(f"Conclusion error-> {e}")
            return None

    def get_paper_summary(self, full_paper):
        paper_summary = {}
        for key, value in full_paper.items():
            paper_summary[key] = value[:300]
        return paper_summary
    
    def check_for_missing_sections(full_paper: Dict[str:str]):
        error_sections = []
        for section_key, section_value in full_paper.items():
            if section_value is None:
                error_sections.append(section_key)
        return error_sections
        