#  AI Research Assistant

An autonomous, AI-powered research tool that generates comprehensive, well-structured research papers on any topic  fully automatically. Enter a topic, and the system plans, searches the web, analyzes sources, writes, and exports a professional `.docx` document.

---

##  Features

-  **Intelligent Planning**  Generates research questions, a structured paper outline, and key concepts using an LLM
-  **Multi-Source Search**  Searches the web (via Tavily) and Wikipedia in parallel with diverse, AI-generated query variations
-  **Deep Source Analysis**  Extracts key findings from up to 12 top-ranked sources using an academic-style LLM prompt
-  **Full Paper Writing**  Writes an Introduction, detailed Body sections, Conclusion, and APA-formatted References
-  **Professional Export**  Saves the output as a formatted `.docx` Word document with correct headings and margins
-  **Streamlit Web UI**  Clean, interactive frontend with live progress updates, source previews, and a one-click download

---

##  Architecture

The system is built around a **LangGraph StateGraph** pipeline. Each stage is an independent agent node that passes state to the next:

```
[Plan] -> [Search] -> [Analyze] -> [Write] -> [Format/Export]
```

```
ai_research_assistant/

+-- app/
   +-- app.py              # Streamlit frontend 

+-- core/
   +-- workflow.py         # LangGraph StateGraph pipeline orchestrator

+-- src_agents/
   +-- planner.py          # PlannerAgent  creates research plan via LLM
   +-- searcher.py         # SearchAgent  parallel web + Wikipedia search
   +-- analyzer.py         # AnalyzerAgent  extracts key findings from sources
   +-- writer.py           # WriterAgent  writes Introduction, Body, Conclusion, References
   +-- format_doc.py       # DocumentGenerator  exports paper as .docx
   +-- scraper.py          # AsyncScraper  async HTTP page scraper (BeautifulSoup)
   +-- content_extractor.py # ContentExtractor  synchronous webpage content extraction


+-- config.py               # API key loader 
+-- requirements.txt        # Python dependencies
+-- .gitignore
+-- README.md
+-- .env.example
```

---

##  How It Works

### 1.  Plan
**`PlannerAgent`** (`src_agents/planner.py`) takes the user's topic and asks an LLM (`openai/gpt-oss-20b` via Groq) to generate:
- Research questions
- A paper outline (sections list)
- Key concepts to explore
- Potential source types

### 2.  Search
**`SearchAgent`** (`src_agents/searcher.py`) first generates diverse query variations of the topic using an LLM, then searches each in parallel using:
- **Tavily** (`advanced` depth, 5 results per query)
- **Wikipedia** (top 5 results)

Results are deduplicated and sorted by relevance score.

### 3.  Analyze
**`AnalyzerAgent`** (`src_agents/analyzer.py`) takes the top 12 ranked sources and, for each one, runs an LLM prompt that extracts objective facts, statistics, and arguments relevant to the research questions. Results are aggregated into a structured markdown format.

### 4.  Write
**`WriterAgent`** (`src_agents/writer.py`) writes the paper in three passes:
1. **Introduction**  context, background, and scope
2. **Body**  deep, section-by-section analysis grounded strictly in the key findings, with inline APA citations
3. **Conclusion**  synthesis, implications, and future directions
4. **References**  APA 7th edition formatted bibliography

> Rate-limit delays are applied between passes to respect Groq API token-per-minute limits.

### 5.  Format & Export
**`DocumentGenerator`** (`src_agents/format_doc.py`) converts the markdown paper into a properly formatted `.docx` file using `python-docx`, with 1-inch margins, centered title, generation date, and heading hierarchy.

---

##  Getting Started

### Prerequisites
- Python 3.10+
- A [Groq](https://console.groq.com/) API key 
- A [Tavily](https://tavily.com/) API key

### Installation

```bash
git clone https://github.com/your-username/ai-research-assistant.git
cd ai-research-assistant
pip install -r requirements.txt
pip install langgraph streamlit   
```

### Environment Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Run the App

```bash
streamlit run app/app.py
```

Open your browser at `http://localhost:8000`, enter a research topic, and click **Start Research**.

---

##  Dependencies

| Package | Purpose |
|---|---|
| `langchain` | Core LLM framework |
| `langchain_groq` | Groq LLM integration |
| `langchain_core` | Prompts, parsers, messages |
| `langchain_community` | Wikipedia tool |
| `langchain_tavily` | Tavily web search |
| `langgraph` | Stateful agent workflow orchestration |
| `streamlit` | Web UI |
| `pydantic` | Structured output validation |
| `python-docx` | `.docx` document generation |
| `beautifulsoup4` | HTML parsing for web scraping |
| `requests` | HTTP requests |
| `wikipedia` | Wikipedia API wrapper |
| `tqdm` | Progress bars |

---

##  Output

Generated papers are saved to the `research_docs/` folder (created automatically) with a timestamped filename:

```
research_docs/The_rise_of_china_as_a_world_power_31_01_2026_15_42_29.docx
```

The Streamlit UI also provides:
- A **download button** for the `.docx` file
- A **Preview tab** with the full paper in markdown
- A **Sources tab** with the top 10 sources used
- A **Findings tab** with key extracted findings per source
- An **Outline tab** with the generated paper structure

---

##  Configuration

API keys are resolved in priority order in `config.py`:
1. `os.getenv()`  system environment variables
2. `os.environ[]`  process-level environment
3. `.env` file  via `python-dotenv`
4. `st.secrets`  Streamlit Cloud secrets

---

##  Notes 

- The workflow sleeps between writing phases to stay within Groq's token-per-minute (TPM) limits.
- Web scraping results depend on whether target sites block automated access (403 errors are handled gracefully).