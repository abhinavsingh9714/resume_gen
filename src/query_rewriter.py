# src/query_rewriter.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.config import GEMINI_MODEL
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class QueryRewriter:
    def __init__(self):
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def rewrite(self, experience: str, job_description: str, style: str) -> str:
        prompt = f"""
Given the following experience and job description, rewrite a concise and information-rich query to retrieve resume writing guidance in the {style.upper()} style:

Experience: {experience}
Job Description: {job_description}
Style: {style.upper()}

Respond only with the rewritten query.
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[QueryRewriter] Error: {e}")
            return f"How to write effective resume bullet points in {style} style"