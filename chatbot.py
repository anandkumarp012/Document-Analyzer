
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# On Streamlit Cloud, read credentials from Streamlit Secrets.
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        model_name = st.secrets.get(
            "GEMINI_MODEL", "gemini-2.5-flash"
        )
    except (KeyError, FileNotFoundError):
        pass

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Configure it in your .env "
        "file locally or in Streamlit Cloud Secrets."
    )

client = genai.Client(api_key=api_key)



def answer_question(question, document_text="", history=None):
    """Answer a user's question using Gemini and the uploaded document."""

    if not question or not question.strip():
        return "Please enter a question."

    if not document_text or not document_text.strip():
        return "Please upload a document first so I can answer questions about it."

    # Limit the document context to avoid sending excessively large prompts.
    document_context = document_text[:30000]

    prompt = f"""
You are an AI document assistant.

Answer the user's question using the provided document.
If the answer is not present in the document, clearly say so.
You may explain related concepts when asked, but distinguish general
knowledge from information explicitly stated in the document.

DOCUMENT:
{document_context}

USER QUESTION:
{question.strip()}
"""

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text or "I couldn't generate an answer. Please try again."

    except Exception as error:
        print(f"Gemini API error: {error}")
        return "Sorry, I couldn't get an answer from Gemini. Check your API key, model name, internet connection, and API quota."
