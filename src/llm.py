import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from prompt_builder import PromptBuilder
from config import GEMINI_MODEL

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_bullets_from_gemini(response):
    try:
        raw_text = response.candidates[0].content.parts[0].text
    except Exception:
        return ["Error: could not parse Gemini response"]

    bullets = re.findall(r"\*\*1\.\s*(.*?)\*\*\s*\*\*2\.\s*(.*?)\*\*", raw_text, re.DOTALL)
    if bullets:
        return [bullets[0][0].strip(), bullets[0][1].strip()]
    fallback = re.findall(r"\*\*(.*?)\*\*", raw_text)
    return fallback[:2] if fallback else [raw_text]

def generate_bullets(experience: str, job_description: str, style: str = "default"):
    try:
        builder = PromptBuilder()
        prompt = builder.build_prompt(experience, job_description, style)

        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)

        return extract_bullets_from_gemini(response)[:2]

    except Exception as e:
        print("Gemini API error:", e)
        return ["Error generating bullet points.", str(e)]