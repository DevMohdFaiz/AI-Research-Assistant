import os
from dotenv import get_key


def _get_groq_api_key():
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if GROQ_API_KEY is None:
        try:
            GROQ_API_KEY = os.environ["GROQ_API_KEY"]
        except KeyError:
            raise "GROQ_API_KEY not set in the environment!"
    return GROQ_API_KEY

def _get_tavily_api_key():
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    if TAVILY_API_KEY is None:
        try:
            TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
        except KeyError:
            raise "TAVILY_API_KEY not set in the environment!"
    return TAVILY_API_KEY   

GROQ_API_KEY =_get_groq_api_key()
TAVILY_API_KEY =_get_tavily_api_key()