import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Set it in .env or Streamlit secrets.")

llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant",
    temperature=0
)