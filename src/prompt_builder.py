import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        content = response.text.strip()
        bullets = [line.strip("-•0123456789. ").strip() for line in content.split("\n") if line.strip()]
        return bullets[:2]

    except Exception as e:
        print("Gemini API error:", e)
        return ["Error generating bullet points.", str(e)]
