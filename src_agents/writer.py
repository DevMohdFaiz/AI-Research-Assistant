import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from tqdm import tqdm
from typing import List, Dict
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



    # def write_section(self, section, key_concepts, key_findings):
    #     prompt = ChatPromptTemplate.from_template("""
    #         You are an expert academic scholar who specializes in writing papers section-wise 
    #         The paper is to be written in different sections and then combined to form a full paper.                                          
    #         You are a single specific section ONLY!
            
    #         Note: Skip the **Introduction** and **Conclusion** sections. Those will be written later on

    #         Key Findings extracted from various sources:
    #         {key_findings}
                                                
    #         Ensure that these concepts are fully explored:
    #         {key_concepts}
            
    #         Write a well-structured, academic section that:
    #         1. Presents information clearly and logically for each section you working on
    #         2. Synthesizes information from multiple sources
    #         3. Maintains an objective, scholarly tone
    #         4. Is approximately 300-500 words
    #         5. Includes proper transitions between ideas
    #         6. Properly cite sources from the given sources
    #         7. Strictly keep your writing based on the given sources
    #         9. Use inline citation where applicable
                                
            
    #         Write the section content (no title needed)
    #         Strictly write the **{section}** section of this paper only. This is highly important!:
    #     """)
    #     chain = prompt | self.llm
    #     try:
    #         response = chain.invoke({
    #             "section": section,
    #             "key_concepts": key_concepts,
    #             "key_findings": key_findings
    #         })
    #         return response.content

    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return f"{section} error-> {e}"
        

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
            print("Finished writing the Introduction")
            return response.content
            
        except Exception as e:
            print(f"Introduction error: {e}")
            return f"# Introduction\n\nThis paper explores {topic}"
        

        
    def write_conclusion(self, topic: str, summary, key_concepts: Dict[str, str]) -> str:
        """Write the conclusion section"""
        prompt = ChatPromptTemplate.from_template("""
            Write a conclusion for this research paper.

            **Topic:** {topic}  

            **Paper Content Summary:**
            {summary}
                                                  
            **Key Concepts**
            {key_concepts}

            Write a strong conclusion (200-350 words) that:
            1. Summarizes key findings
            2. Synthesizes main insights
            3. Discusses implications
            4. Suggests future directions

            Write the conclusion:
        """)
        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "topic": topic, "summary": summary, "key_concepts": key_concepts
            })
            print("Finished writing the conclusion")
            return response.content
        
        except Exception as e:
            print(f"Conclusion error-> {e}")
            return f"This paper has explored the folowing:\n {key_concepts}"
 

    def write_references(self, paper_sources):
        """"Write the paper references in APA format"""
        references_prompt = ChatPromptTemplate.from_template("""
            You are an expert Academic Librarian and Citation Specialist.
            Your task is to compile a strictly formatted **References** section for a research paper.

            ### INPUT SOURCES
            Here is the raw list of sources used in the research:
            {paper_sources}

            ### FORMATTING RULES (APA 7th Edition)
            1.  **Header:** The section must be titled "**References**" (centered, bold).
            2.  **Sorting:** Sort all entries **alphabetically** by the first author's surname (or title if no author).
            3.  **Structure:** Follow this exact pattern for each entry:
                * *Author, A. A. (Year, Month Day). Title of page. Site Name. URL*
                * If no author is listed, use: *Title of page. (Year, Month Day). Site Name. URL*
                * If no date is listed, use: *(n.d.)*.
            4.  **No Hallucinations:** Do not invent authors or dates. If metadata is missing in the input, use reasonable defaults (e.g., "n.d." for no date) based strictly on the provided info.
            5.  **Clean Output:** Output **only** the references list. Do not add introductory text like "Here are your references or "References""

            ### GENERATE
            Compile the references list now:
        """)

        llm = ChatGroq(api_key= GROQ_API_KEY_2, model="llama-3.3-70b-versatile", temperature=0.1)
        chain = references_prompt | llm

        try:
            references_response =  chain.invoke({"paper_sources": paper_sources})
            print("Finished writing the references section")
            return references_response.content
        except Exception as e:
            print(f"Error writing references-> {e}")
            return f"references error-> {e}"


    def get_paper_summary(self, full_paper):
        """Summarize the paper for the llm to write the conclusion"""
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
    

    def write_paper(self, topic, plan, key_findings, parsed_key_findings):
        """Write the complete paper"""
        full_paper = {}
        key_concepts = plan["key_concepts"]
        paper_outline = plan["paper_outline"]

        print(f"Writing the introduction...")
        introduction = self.write_introduction(topic, key_concepts, paper_outline)
        full_paper['introduction'] = introduction 

        print("Sleeping for 65 secs to respect rate limit")
        for _ in tqdm(range(1, 66), desc="Sleeping to respect rate limit"):
            time.sleep(1)

        print("Writing the Body of the paper...")
        paper_body = self.write_body(parsed_key_findings, key_concepts, paper_outline)
        full_paper['body'] = paper_body

        print("Sleeping for 65 secs to respect rate limit")
        for _ in tqdm(range(1, 66), desc="Sleeping to respect rate limit"):
            time.sleep(1)

        print("Writing the conclusion...\n")
        paper_summary = self.get_paper_summary(full_paper)
        conclusion = self.write_conclusion(topic, paper_summary, key_concepts)
        full_paper['conclusion'] = conclusion

        print("Writing references\n")
        paper_sources = [k['url'] for k in key_findings]
        paper_references = self.write_references(paper_sources)
        full_paper['references'] = paper_references

        final_doc = self.parse_paper_to_string(topic, full_paper) #parse the whole paper to a string

        return final_doc

    
    
    def write_body(self, key_findings, key_concepts, paper_outline):
        """Write the body of the paper excluding the introduction and references"""
        system_content = f"""
            You are a Senior Academic Research Fellow.
            Your task is to write the **BODY CONTENT ONLY** for a high-impact research paper.

            ### STRICT PROHIBITIONS (CRITICAL)
            1.  **NO METADATA:** Do NOT write a Title, Author Name, Abstract, or Keywords.
            2.  **NO INTRO/OUTRO:** Do NOT write the Introduction or Conclusion sections. Start immediately with the first body section from the Outline.
            3.  **NO SURFACE-LEVEL SUMMARIES:** Do not just list facts. You must explain *why* they matter, the *causal mechanisms* behind them, and their *implications*.
            4.  **NO HALLUCINATION:** Base all arguments strictly on the provided Key Findings.
            5.  **CLEAN OUTPUT**: Do not add any extra introductory text like "Body" or "Here is the body of the paper"

            ### DEPTH & STYLE REQUIREMENTS
            1.  **Maximize Depth:** For every claim you make, provide the evidence (citation) and the implication.
            2.  **Scholarly Density:** Use precise academic terminology. Avoid "fluff" words.
            3.  **Paragraph Structure:** Each paragraph must have a clear claim, supporting evidence from the data, and critical analysis.
            4.  **Word Count:** Aim to be as comprehensive and detailed as possible for each section.
            5.  **Citations:** Use inline citations in APA format derived strictly from the Key Findings.
            6.  **Continuity:** Ensure smooth logical transitions between the sections defined in the Outline.

            ### DATA SOURCE (THE TRUTH)
            {key_findings}

            ### REQUIRED CONCEPTS
            {key_concepts}
        """       

        user_content = f"""
            ### EXECUTION ORDER
            Write the **BODY SECTIONS** of the paper strictly following this Outline.

            **OUTLINE:**
            {paper_outline}

            **INSTRUCTION:**
            Start writing immediately.
            1. Begin directly with the first header in the outline.
            2. Ensure you cover every bullet point in the outline with deep analysis.
            3. Do not stop until all outline sections are complete.
        """

        print(f"Sending system context to Groq cache\n")

        try:
            llm = ChatGroq(api_key=GROQ_API_KEY_2, model="openai/gpt-oss-120b", temperature=0.4, max_retries=0)
            llm.invoke(
                [
                    SystemMessage(content=system_content),
                    HumanMessage(content="Reply OK")
                ],
                max_tokens= 2
            )
            print("System prompt uploaded to cache")
        except Exception as e:
            print(f"Failed to upload to cache-> {e}")
            return {"error": f"error uploading system content-> {e}"}

        print("Waiting 70 secs for max token limit")        
        for _ in tqdm(range(1, 71), desc="Sleeping to respect rate limit"):
            time.sleep(1)

        print(f"Writing full paper...")

        try:
            final_paper = llm.invoke(
                [
                    SystemMessage(content=system_content),
                    HumanMessage(content= user_content)
                ]
            )
            print("Finished writing paper :)")
            return final_paper.content
        
        except Exception as e:
            print(f"Error writing paper-> {e}")
            return f"error writing paper-> {e}"

        
    
    def parse_paper_to_string(self, topic, full_paper):
        """Parse the complete paper"""
        final_doc = ""
        final_doc += f"# {topic}\n\n"
        for section, content in full_paper.items():
            final_doc += f"## {section.capitalize()}\n{content}\n"
        return final_doc
    
  
        