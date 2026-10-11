import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# --------------------------------------------------
# Gemini
# --------------------------------------------------

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
    google_api_key=GOOGLE_API_KEY,
    max_retries=0,
)


# --------------------------------------------------
# Groq
# --------------------------------------------------

groq_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY,
)


# --------------------------------------------------
# SQL LLM
# --------------------------------------------------

sql_llm = gemini_llm.with_fallbacks([groq_llm])