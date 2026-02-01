from langgraph.graph import add_messages
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

    messages: Annotated[List[BaseMessage], add_messages]



#     from langgraph.graph import StateGraph, END
# from core.workflow import ResearchState
# from src_agents import format_doc, planner, scraper, analyzer, searcher, writer


# def create_workflow():
#     planner_agent = planner.PlannerAgent(model="llama-3.3-70b-versatile")
#     search_agent = searcher.SearchAgent()
#     # scraper_agent = scraper.ScraperAgent()
#     analyzer_agent = analyzer.AnalyzerAgent()
#     writer_agent = writer.WriterAgent()
#     doc_formatter = format_doc.DocumentGenerator()

#     workflow = StateGraph(ResearchState)

#     # ============================================
#     # NODE 1: PLAN
#     # ============================================
#     def plan_node(state: ResearchState):
#         """Create the research plan"""
#         plan = planner_agent.create_plan(state["topic"])

#         print(f"Created plan\n")
#         print(f"Research Questions: {plan['research_questions']}")
#         print(f"Paper Outline: {plan['paper_outline']}")

#         # Return ONLY updated keys
#         return {
#             "research_plan": plan,
#             "research_questions": plan["research_questions"],
#             "paper_outline": plan["paper_outline"],
#             "key_concepts": plan["key_concepts"]
#         }

#     # ============================================
#     # NODE 2: SEARCH
#     # ============================================
#     def search_node(state: ResearchState):
#         """Search using planner's research questions"""
#         search_results = search_agent.fast_search(
#             state["topic"]
#         )

#         print(f"Found {len(search_results)} sources")

#         # Return ONLY updated keys
#         return {
#             "search_results": search_results
#         }

#     # ============================================
#     # NODE 3: SCRAPE
#     # ============================================
#     # def scrape_node(state: ResearchState):
#     #     """Scrape full content from sources"""
#     #     enriched = scraper_agent.scrape_sources(state["search_results"])

#     #     print(f"Scraped {len(enriched)} sources")

#     #     # Return ONLY updated keys
#     #     return {
#     #         "search_results": enriched
#     #     }

#     # ============================================
#     # NODE 4: ANALYZE
#     # ============================================
#     def analyze_node(state: ResearchState):
#         """Analyze sources and extract key findings"""
#         key_findings, parsed_key_findings = analyzer_agent.analyze_sources(
#             state["search_results"][:12],
#             state["research_questions"]
#         )

#         print(f"Extracted {len(parsed_key_findings)} key findings")

#         # Return ONLY updated keys
#         return {
#             "key_findings": parsed_key_findings
#         }

#     # ============================================
#     # NODE 5: WRITE
#     # ============================================
#     def write_node(state: ResearchState):
#         """Write paper using findings"""
#         full_paper = writer_agent.write_paper(
#             state["topic"],
#             state["research_plan"],
#             state["key_findings"]
#         )

#         print(f"Full paper written!")

#         # Return ONLY updated keys
#         return {
#             "full_paper": full_paper
#         }

#     # ============================================
#     # NODE 6: FORMAT
#     # ============================================
#     def format_node(state: ResearchState):
#         """Format and save paper"""
#         output_path = doc_formatter.generate_docx(
#             state["full_paper"],
#             state["topic"]
#         )

#         print(f"Saved paper to {output_path}")

#         # Return ONLY updated keys
#         return {
#             "output_path": output_path
#         }

#     # ============================================
#     # BUILD GRAPH
#     # ============================================
#     workflow.add_node("plan", plan_node)
#     workflow.add_node("search", search_node)
#     # workflow.add_node("scrape", scrape_node)
#     workflow.add_node("analyze", analyze_node)
#     workflow.add_node("write", write_node)
#     workflow.add_node("format", format_node)

#     workflow.set_entry_point("plan")
#     workflow.add_edge("plan", "search")
#     workflow.add_edge("search", "analyze")
#     # workflow.add_edge("scrape", "analyze")
#     workflow.add_edge("analyze", "write")
#     workflow.add_edge("write", "format")
#     workflow.add_edge("format", END)

#     return workflow.compile()
# topic = "The politics of Xi Jingping"

# workflow = create_workflow()
# result = workflow.invoke(initial_state)
    