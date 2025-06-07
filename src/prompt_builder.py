import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_bullets_from_gemini(response):
    try:
        raw_text = response.candidates[0].content.parts[0].text
    except Exception:
        return ["Error: could not parse Gemini response"]
    print("Raw text from Gemini response:", raw_text)
    # Extract text between "**1." and "**2.", "**2." to end
    bullets = re.findall(r"\*\*1\.\s*(.*?)\*\*\s*\*\*2\.\s*(.*?)\*\*", raw_text, re.DOTALL)

    if bullets:
        return [bullets[0][0].strip(), bullets[0][1].strip()]
    else:
        # fallback: match any bolded lines
        fallback = re.findall(r"\*\*(.*?)\*\*", raw_text)
        return fallback[:2] if fallback else [raw_text]
    
def generate_bullets(experience: str, job_description: str, style: str):
    style_instructions = {
        "default": "Use a clear, professional tone.",
        "concise": "Use a compact, to-the-point tone with minimal filler.",
        "metrics": "Prioritize quantifiable impact and performance metrics.",
        "leadership": "Highlight leadership, collaboration, and decision-making.",
        "action": "Use strong action verbs to convey initiative and ownership."
    }

    tone = style_instructions.get(style, style_instructions["default"])

    prompt = f"""
You are a professional resume writer.

Convert the following work experience into 2 recruiter-optimized, ATS-friendly bullet points for a professional resume.

Apply the following tone: {tone}

Experience:
{experience}

Target Job Description:
{job_description}

Output:
1.
2.
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-001")
        response = model.generate_content(prompt)
        # print("Gemini API response:", response)
        # content = response.text.strip()
        bullets = extract_bullets_from_gemini(response)
        return bullets[:2]

    except Exception as e:
        print("Gemini API error:", e)
        return ["Error generating bullet points.", str(e)]
