import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from src.prompt_builder import PromptBuilder
from src.config import GEMINI_MODEL

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

def generate_bullets(experience: str, job_description: str, style: str = "STAR"):
    try:
        builder = PromptBuilder(use_gemini=True)
        prompt = builder.build_prompt(experience, job_description, style)

        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)

        return extract_bullets_from_gemini(response)[:2]

    except Exception as e:
        print("Gemini API error:", e)
        return ["Error generating bullet points.", str(e)]
    

if __name__ == "__main__":
    # Example usage
    # experience = "Led a team of 5 engineers to develop a new feature that increased user engagement by 30%."
    experience = '''Designed and deployed a multi-modal Machine Learning based baby monitoring system to monitor baby activities and provide real-time alerts to parents from live video feed of the room. Developed a two-tier object detection pipeline using RCNN Detectron2 model to detect general objects in the room, including humans, mobiles, and cribs. The regions of interest (ROIs) for detected humans are then passed to a custom-trained YOLOv8 model, which classifies them as adults or babies achieving highly accurate detection of the baby, even in challenging conditions such as 80%-90% partial occlusion and low lighting. Implemented a video-based baby sleep tracker using frame-by-frame computational logic over human pose from MediaPipe pose detection to detect subtle movements of baby in real time, detecting sleep status even when the baby is 80% covered. Engineered a cry detection model by fine-tuning a Yamnet MediaPipe audio detector on live microphone inputs, enabling the system to accurately recognize baby cries in real time with less than 13ms latency. Fine-tuned BLIP VQA model to monitor and count baby diaper changes over time from live video feeds, enhancing the system’s utility for parents. Developed a RetinaFace-based face blurring module, which anonymizes faces of the baby and adults in the video stream to protect the privacy. Built an API using FastAPI to process video streams, sending them through a machine learning pipeline with outputs returned in JSON format. Containerized the entire system using Docker and deployed it on an AWS EC2 Linux machine for scalable, real-time performance.
                    '''
    # job_description = "Looking for a software engineer with strong leadership skills and a track record of delivering impactful features."
    job_description = '''The ideal candidate will have industry experience working on a range of recommendation, classification, and optimization problems. You will bring the ability to own the whole ML life cycle, define projects and drive excellence across teams. You will work alongside the world’s leading engineers and researchers to solve some of the most exciting and massive social data and prediction problems that exist on the web. Software Engineer, Machine Learning Responsibilities: Leading projects or small teams of people to help them unblock, advocating for ML excellence. Adapt standard machine learning methods to best exploit modern parallel environments (e.g. distributed clusters, multicore SMP, and GPU). Develop highly scalable classifiers and tools leveraging machine learning, data regression, and rules based models. Suggest, collect and synthesize requirements and create effective feature roadmaps. Code deliverables in tandem with the engineering team. Minimum Qualifications: 6+ years of experience in software engineering or a relevant field. 3+ years of experience if you have a PhD2+ years of experience in one or more of the following areas: machine learning, recommendation systems, pattern recognition, data mining, artificial intelligence, or a related technical field. Experience with scripting languages such as Python, Javascript or Hack. Experience with developing machine learning models at scale from inception to business impact. Knowledge developing and debugging in C/C++ and Java, or experience with scripting languages such as Python, Perl, PHP, and/or shell scripts. Experience building and shipping high quality work and achieving high reliability. Track record of setting technical direction for a team, driving consensus and successful cross-functional partnerships. Experience improving quality through thoughtful code reviews, appropriate testing, proper rollout, monitoring, and proactive changes. Bachelor degree in Computer Science, Computer Engineering, relevant technical field, or equivalent practical experience. Preferred Qualifications Masters degree or PhD in Computer Science or another ML-related field. Exposure to architectural patterns of large scale software applications. Experience with scripting languages such as Pytorch and TF
                        '''
    bullets = generate_bullets(experience, job_description, style="xyz")
    print("Generated Bullets:")
    for bullet in bullets:
        print(f"- {bullet}")