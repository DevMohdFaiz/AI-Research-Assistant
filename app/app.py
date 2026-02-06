import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import streamlit as st
from pathlib import Path
from core.workflow import create_workflow
from src_agents.format_doc import DocumentGenerator


st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.75rem;
        font-size: 1.1rem;
        border-radius: 8px;
        border: none;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .status-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    .status-planning {
        background-color: #e3f2fd;
        border-color: #2196F3;
    }
    .status-searching {
        background-color: #fff3e0;
        border-color: #FF9800;
    }
    .status-analyzing {
        background-color: #f3e5f5;
        border-color: #9C27B0;
    }
    .status-writing {
        background-color: #e8f5e9;
        border-color: #4CAF50;
    }
    .status-complete {
        background-color: #e8f5e9;
        border-color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'research_running' not in st.session_state:
    st.session_state.research_running = False
if 'result' not in st.session_state:
    st.session_state.result = None
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = None

# Header
st.title("AI Research Assistant")
st.markdown("**Generate comprehensive research papers automatically**")
st.markdown("---")

# Sidebar
with st.sidebar:    
    st.markdown("### How it works")
    st.markdown("""
    1. **Plan**: Generates research questions & outline
    2. **Search**: Finds and extracts relevant sources from the web
    4. **Analyze**: Identifies key findings
    5. **Write**: Creates structured paper
    6. **Format**: Exports professional document to .docx file
    """)
    
    st.markdown("---")
    st.markdown("### Tips")
    st.markdown("""
    - Be specific with your topic
    - Include key terms you want covered
    """)


col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Enter Your Research Topic")
    
    topic = st.text_input(
        "Research Topic",
        placeholder="Research Topic",
        help="Enter the topic you want to research",
        label_visibility="collapsed"
    )
    
    st.session_state.selected_topic = topic

    if 'selected_topic' in st.session_state:
        topic = st.session_state.selected_topic
        del st.session_state.selected_topic


# Research button
if st.button("Start Research", disabled=st.session_state.research_running or not topic):
    st.write("hello")
    if topic:
        st.session_state.research_running = True
        st.session_state.result = None
        st.rerun()

# Progress section
if st.session_state.research_running:
#     st.markdown("---")
#     st.subheader("Research in Progress")
    
#     progress_container = st.container()
#     status_container = st.container()
    
#     with progress_container:
#         progress_bar = st.progress(0) 
#         status_text = st.empty()
    
#     with status_container:
#         stage_display = st.empty()


    class Logger:
        def write(self, text):
            if text.strip():
                st.write(text.strip())
        def flush(self):
            pass

    old_stdout = sys.stdout
    sys.stdout = Logger()
   
    with st.status("Running research...", expanded=True) as status:
        try:
            start_time = time.time()
            workflow = create_workflow()

            initial_state = {
                "topic": topic,
                "plan": {},
                "research_questions": [],
                "paper_outline": [],
                "key_concepts": [],
                "search_results": [],
                "key_findings": [],
                "full_paper": "",
                "output_path": ""
            }
            
            result = workflow.invoke(initial_state)
            st.write(f"Time taken: {((time.time() - start_time) / 60):.2f} mins")

            sys.stdout = old_stdout
            status.update(label= "Research Complete!", state="complete")

            st.session_state.result = {
                'path': result["output_path"],
                'paper': result["full_paper"],
                'sources': result["search_results"],
                'findings': result["key_findings"],
                'outline': result["paper_outline"],
                'time_taken': time.time() - start_time
            }
            st.session_state.research_running = False
            st.rerun()
        
        except Exception as e:
            sys.stdout = old_stdout
            status.update(label="Error", state="error")
            st.error(f"Error during research: {str(e)}")
            st.session_state.research_running = False


if st.session_state.result and not st.session_state.research_running:
    st.markdown("---")
    st.success(f"Research Complete! | Time taken: {((st.session_state.result['time_taken']) / 60):.2f} mins")
    
    # Download button
    with open(st.session_state.result['path'], 'rb') as f:
        st.download_button(
            label="Download Research Paper",
            data=f,
            file_name=Path(st.session_state.result['path']).name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document" 
        )
    
   
    tab1, tab2, tab3, tab4 = st.tabs(["Preview", "Sources", "Findings", "Outline"])
    
    with tab1:
        st.markdown("### Paper Preview")
        st.markdown(st.session_state.result['paper'])
    
    with tab2:
        st.markdown("### Sources Used")
        for i, source in enumerate(st.session_state.result['sources'][:10], 1):
            with st.expander(f"{i}. {source.get('title', 'Unknown')}"):
                st.markdown(f"**URL**: {source.get('url', 'N/A')}")
                st.markdown(f"**Type**: {source.get('type', 'web')}")
                if source.get('content'):
                    st.markdown("**Preview**:")
                    st.text(source['content'][:300] + "...")
    
    with tab3:
        st.markdown("### Key Findings")
        for i, finding in enumerate(st.session_state.result['findings'], 1):
            with st.expander(f"{finding.get('title', 'Unknown Source')}"):
                st.markdown(finding.get('key_points', 'No details available'))
    
    with tab4:
        st.markdown("### Paper Outline")
        for i, section in enumerate(st.session_state.result['outline'], 1):
            st.markdown(f"{i}. **{section}**")
    
    # New research button
    if st.button("Start New Research"):
        st.session_state.result = None
        st.rerun()

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 2rem;'>
    <p>Generate comprehensive research papers automatically</p>
    <p>Copyright 2026</p>
</div>
""", unsafe_allow_html=True)