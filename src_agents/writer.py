import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from tqdm import tqdm
from config import GROQ_API_KEY_2, GROQ_API_KEY


class WriterAgent:
    """Write the full paper section-wise""" 

    def __init__(self, model="openai/gpt-oss-120b"):
        self.llm = ChatGroq(api_key= GROQ_API_KEY, model=model, temperature=0.1)

    
    # def write_sections(self, sections, key_concepts, key_findings):
    #     full_paper_sections = {}
    #     for idx, section in tqdm(enumerate(sections), desc="Wrtting sections...", total=len(sections)):
    #         if section.lower() not in ["introduction", "conclusion"]:
    #             full_paper_sections[section] = self._write_section(section, key_concepts, key_findings)
    #             time.sleep(2)
    #     return full_paper_sections



    def write_section(self, section, key_concepts, key_findings):
        prompt = ChatPromptTemplate.from_template("""
            You are an expert academic scholar who specializes in writing papers section-wise 
            The paper is to be written in different sections and then combined to form a full paper.                                          
            You are a single specific section ONLY!
            
            Note: Skip the **Introduction** and **Conclusion** sections. Those will be written later on

            Key Findings extracted from various sources:
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
                                
            
            Write the section content (no title needed)
            Strictly write the **{section}** section of this paper only. This is highly important!:
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
            return f"This paper has explored the folowing:\n {sections}"

    def get_paper_summary(self, full_paper):
        paper_summary = {}
        for key, value in full_paper.items():
            paper_summary[key] = value[:300]
        return paper_summary
    
    def check_for_missing_sections(self, full_paper: Dict):
        error_sections = []
        for section_key, section_value in full_paper.items():
            if section_value is None:
                error_sections.append(section_key)
        return error_sections
    

    def write_paper(self, topic, plan, key_findings):
        """Write the complete paper"""
        full_paper = {}
        key_concepts = plan["key_concepts"]
        paper_outline = plan["paper_outline"]

        print(f"Writing the introduction...")
        introduction = self.write_introduction(topic, key_concepts, key_findings)
        full_paper['introduction'] = introduction 
        if full_paper['introduction'] is not None:
            print(f"Finished writing the introduction!")

        for section in paper_outline:
            if section.lower() not in ["introduction", "conclusion"]:
                print(f"Writing **{section}** section...")
                full_paper[section] = self.write_section(section, key_concepts, key_findings)
                if full_paper[section] is not None:
                    print(f"Finished writing **{section}**") #keep track of written section

        paper_summary = self.get_paper_summary(full_paper)
        conclusion = self.write_conclusion(topic, paper_summary, paper_outline)
        full_paper['conclusion'] = conclusion
        if full_paper['conclusion'] is not None:
            print(f"Finished writing the conclusion!")

        missing_sections = self.check_for_missing_sections(full_paper) #check for missing sections
        print(f"Found {len(missing_sections)} missing sections-> {missing_sections}")
        if len(missing_sections) > 0:
            for section in missing_sections:
                if section.lower() == "introduction":
                    introduction = self.write_introduction(topic, key_concepts, key_findings)
                    full_paper['introduction'] = introduction 
                elif section.lower() == "conclusion":
                    conclusion = self.write_conclusion(topic, paper_summary, paper_outline)
                    full_paper['conclusion'] = conclusion
                else:
                    full_paper[section] = self.write_section(section)

        final_doc = self.parse_paper_to_string(topic, full_paper) #parse the whole paper to a string

        return final_doc

    def parse_paper_to_string(self, topic, full_paper):
        """Parse the complete paper"""
        final_doc = ""
        final_doc += f"# {topic}\n\n"
        for section, content in full_paper.items():
            final_doc += f"## {section.capitalize()}\n{content}\n"
        return final_doc
    
    def play_func():
        return "hello"
        