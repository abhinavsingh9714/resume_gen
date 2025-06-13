from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv
from src.llm import generate_bullets

load_dotenv()

app = FastAPI(title="Resume Bullet Generator")

class ExperienceInput(BaseModel):
    experience: str = Field(..., min_length=0)
    job_description: str = Field(..., min_length=0)
    style: Optional[str] = Field(default="default", description="Choose from: default, concise, metrics, leadership, action")

class BulletPointOutput(BaseModel):
    bullets: List[str]

@app.post("/generate-bullets", response_model=BulletPointOutput)
def generate_resume_bullets(payload: ExperienceInput):
    if not payload.experience or not payload.job_description:
        raise HTTPException(status_code=400, detail="Experience and Job Description are required")

    bullets = generate_bullets(payload.experience, payload.job_description, payload.style)
    return {"bullets": bullets}
