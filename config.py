import os
import streamlit as st
from dotenv import get_key


def _get_groq_api_key():
    """Get the groq api key from .env"""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if GROQ_API_KEY is None:
        try:
            GROQ_API_KEY = os.environ["GROQ_API_KEY"]
        except KeyError:  
            GROQ_API_KEY = get_key(".env", "GROQ_API_KEY")  
            if GROQ_API_KEY is None:
                GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
        except Exception as e:
            raise KeyError(f"GROQ_API_KEY not set in the environment! -> {e}")
    return GROQ_API_KEY
    
def _get_groq_api_key_2():
    """Get the groq api key from .env"""
    GROQ_API_KEY_2 = os.getenv("GROQ_API_KEY_2")
    if GROQ_API_KEY_2 is None:
        try:
            GROQ_API_KEY_2 = os.environ["GROQ_API_KEY_2"]
        except KeyError:
            GROQ_API_KEY_2 = get_key(".env", "GROQ_API_KEY_2") 
            if GROQ_API_KEY_2 is None:
                GROQ_API_KEY_2 = st.secrets["GROQ_API_KEY_2"]
        except Exception as e:
            raise KeyError(f"GROQ_API_KEY_2 not set in the environment! -> {e}")
    return GROQ_API_KEY_2

def _get_tavily_api_key():
    """Get the tavily api key from .env"""
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    if TAVILY_API_KEY is None:
        try:
            TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
        except KeyError:
            TAVILY_API_KEY = get_key(".env", "TAVILY_API_KEY") 
            if TAVILY_API_KEY is None:
                TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
        except Exception as e:
            raise KeyError(f"TAVILY_API_KEY not set in the environment! -> {e}")
    return TAVILY_API_KEY   

GROQ_API_KEY =_get_groq_api_key()
GROQ_API_KEY_2 =_get_groq_api_key_2()
TAVILY_API_KEY =_get_tavily_api_key()