# src/query_rewriter.py
# import google.generativeai as genai
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
from src.config import GEMINI_MODEL
load_dotenv()

if 'GEMINI_API_KEY' not in os.environ:
    print('api key not found')

llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

class QueryRewriter:
    def __init__(self):
        # self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.model = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    def rewrite(self, experience: str, job_description: str, style: str) -> str:
        messages = [
            SystemMessage(content=f"You are given a job description and experience. Rewrite a concise and information-rich query to retrieve resume writing guidance in the {style.upper()} style."),
            HumanMessage(content=f"Experience: {experience}"),
            HumanMessage(content=f"Job Description: {job_description}")
        ]

        response = self.model.invoke(messages)
        return response.content.strip()

#         prompt = f"""
# Given the following experience and job description, rewrite a concise and information-rich query to retrieve resume writing guidance in the {style.upper()} style:

# Experience: {experience}
# Job Description: {job_description}
# Style: {style.upper()}

# Respond only with the rewritten query.
# """
#         try:
#             response = self.model.generate_content(prompt)
#             return response.text.strip()
#         except Exception as e:
#             print(f"[QueryRewriter] Error: {e}")
#             return f"How to write effective resume bullet points in {style} style"


if __name__ == "__main__":
    rewriter = QueryRewriter()
    # result = rewriter.rewrite(
    #     experience="Led a team of software engineers to deliver a scalable web application.",
    #     job_description="Seeking a candidate with leadership experience and web development skills.",
    #     style="professional"
    # )
    result = rewriter.rewrite('1+ year of experience working as a data scientist developing data pipelines','write scalabe ml pipelines in pytorch','star')
    print(result)