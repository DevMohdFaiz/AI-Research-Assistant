from langgraph.graph import StateGraph, END, add_messages
from src_agents import format_doc, planner, content_extractor, scraper, analyzer, searcher, writer
from langchain_core.messages import BaseMessage
from typing import List, Dict, Annotated, TypedDict

class ResearchState(TypedDict):
    """Overall state for the research workflow"""
    topic: str
    research_plan: Dict
    research_questions: List
    paper_outline: List
    key_concepts: List
    search_results: List
    key_findings: List
    parsed_key_findings: List
    full_paper: str
    output_path: str

    # messages: Annotated[List[BaseMessage], add_messages]


def create_workflow():
    planner_agent = planner.PlannerAgent(model="llama-3.3-70b-versatile")
    search_agent = searcher.SearchAgent()
    analyzer_agent = analyzer.AnalyzerAgent()
    writer_agent = writer.WriterAgent()
    doc_formatter = format_doc.DocumentGenerator()

    workflow = StateGraph(ResearchState)

    def plan_node(state: ResearchState):
        """Create the research plan"""
        print("Creating research plan...")
        plan = planner_agent.create_plan(
            state["topic"]
        )

        print(f"Created research plan\n")
        print(f"Research Questions: {plan['research_questions']}")
        print(f"Paper outline: {plan['paper_outline']}")
         
        return {
            "research_plan": plan,
            "research_questions": plan["research_questions"],
            "paper_outline": plan["paper_outline"],
            "key_concepts": plan["key_concepts"]

        }
    
    def search_node(state: ResearchState):
        """Search for sources"""
        print("Searching for sources...")
        search_results = search_agent.search(
            state["topic"],
            sort_results=True
        )

        print(f"Searched for {len(search_results)} sources")
        return {
            "search_results": search_results 
        }
    
    def analyze_node(state: ResearchState):
        """Analyze the sources and extract key points"""
        print("Analyzing sources...")
        key_findings, parsed_key_findings = analyzer_agent.analyze_sources(
            state['search_results'][:12], #only use the first 12 ranked sources
            state["research_questions"]
        )
        
        print(f"Extracted {len(parsed_key_findings):,} key findings from sources")
        return {
            "key_findings": key_findings,
            "parsed_key_findings": parsed_key_findings,
        }
    
    def write_node(state: ResearchState):
        """Write the full paper"""
        full_paper = writer_agent.write_paper(
            state["topic"],
            state["research_plan"],
            state["key_findings"],
            state["parsed_key_findings"]
        )
        # full_paper = writer_agent.write_paper(topic, plan, key_findings, parsed_key_findings)

        print(f"Full paper written!")
        return {
            "full_paper": full_paper
        }
    
    def format_node(state: ResearchState):
        """Format and save the paper as a docx file"""
        print("Saving paper...")
        output_path = doc_formatter.generate_docx(
            state["full_paper"],
            state["topic"]
        )
        
        print(f"Saved paper to {output_path}")
        return {
            "output_path": output_path
        }

    workflow.add_node("plan", plan_node)
    workflow.add_node("search", search_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("write", write_node)
    workflow.add_node("format", format_node)


    workflow.set_entry_point("plan")
    workflow.add_edge("plan", "search")
    workflow.add_edge("search", "analyze")
    workflow.add_edge("analyze", "write")
    workflow.add_edge("write", "format")
    workflow.add_edge("format", END)
    
    return workflow.compile()