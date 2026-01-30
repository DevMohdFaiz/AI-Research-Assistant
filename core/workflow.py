from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing import List, Dict, Annotated, TypedDict

class ResearchState(TypedDict):
    """Overall state for the research workflow"""

    topic: str
    research_questions: List
    paper_outline: List
    key_concepts: List

    search_results: Dict
    key_findings: Dict
    full_paper: Dict
    final_doc: str

    messages: Annotated[List[BaseMessage], add_messages]
    