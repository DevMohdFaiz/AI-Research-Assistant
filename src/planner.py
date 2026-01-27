import json
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config import GROQ_API_KEY

def create_plan(topic: str):
    """Create a plan for the research workflow"""
    prompt = ChatPromptTemplate.from_template("""
    You are an expert research planner. Create a comprehensive research plan for this topic:

    Topic: {topic}

    Provide:
    1. Research questions (5-7 key questions to answer)
    2. Outline (main sections for the paper)
    3. Key concepts to explore
    4. Potential sources to look for

    Format your answer as JSON:
    {{
        "research_questions": ["question1", "question2", "question3", ... question_N],
        "outline": ["Introduction", "Section1", "Section2", ..., "Conclusion"],
        "key_concepts": [...],
        "source_types": [...]
    }}
    DO NOT ADD ANYTHING ELSE TO THE JSON
    """)
    llm = ChatGroq(api_key=GROQ_API_KEY, temperature=0.8, model="openai/gpt-oss-120b")
    chain = prompt | llm | JsonOutputParser()

    try:
        response = chain.invoke(topic)
        return response 

    except Exception as e:
        print(f"Planner Error {e}")
        return {
                    "research_questions": [
                        f"What is {topic}?",
                        f"Why is {topic} important?",
                        f"What are the key aspects of {topic}?",
                        f"What are current developments in {topic}?",
                        f"What are future implications of {topic}?"
                    ],
                    "outline": [
                        "Introduction",
                        "Background and Context",
                        "Main Analysis",
                        "Current State",
                        "Future Directions",
                        "Conclusion"
                    ],
                    "key_concepts": [topic],
                    "search_queries": [
                        topic,
                        f"{topic} overview",
                        f"{topic} recent developments"
                    ]
                }

    