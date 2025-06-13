# Resume Bullet Generator

A FastAPI-powered service that generates **ATS-optimized**, **quantified**, and **job-tailored** resume bullet points using a hybrid approach of:
- **Semantic retrieval from a curated knowledge base**
- **Gemini-based prompt rewriting and LLM generation**

## Features

- **High-Impact Resume Bullet Generation** using XYZ, STAR, or custom styles
- **Semantic Knowledge Base Retrieval** with FAISS + Sentence Transformers
- **Gemini-Powered Query Rewriting** to craft smarter context-aware prompts
- **LLM Bullet Generation** with result post-processing and fallback logic
- **Test Coverage** with pytest for key components
- **Modular Design** for clean integration and experimentation

---

## Project Structure

```resume_gen/
├── kb_chunks/ # Chunked knowledge base (.jsonl)
├── kb_index/ # FAISS index files
├── knowledge_base/ # Raw .txt resume writing guides
├── src/
│ ├── config.py # Config paths and constants
│ ├── embed_and_store.py # Embedding + FAISS indexing script
│ ├── retriever.py # FAISS + transformer-based retriever
│ ├── query_rewriter.py # Gemini-based query enhancer
│ ├── prompt_builder.py # Prompt construction logic
│ ├── llm.py # Gemini LLM integration and response parsing
│ ├── main.py # FastAPI server
│ └── feedback.py # (Optional) User feedback tracking
├── tests/ # Unit tests with pytest
├── requirements.txt
└── README.md```

---

## Setup Instructions

### 1. Clone and Setup Environment

```git clone https://github.com/yourname/resume-gen.git
cd resume-gen
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt```

### 2. Set Environment Variables
Create a .env file in the root directory:

'''
GEMINI_API_KEY=your_google_generative_ai_key
GEMINI_MODEL=gemini-pro
'''
### 3. Embed Knowledge Base and Build FAISS Index
'''
python resume_gen/src/embed_and_store.py
'''
This reads kb_chunks/knowledge_base.jsonl, computes sentence embeddings, and saves the FAISS index to kb_index/faiss.index.

### 4. Run the FastAPI Server
'''
uvicorn resume_gen.src.main:app --reload
'''
Visit: http://localhost:8000/docs for the Swagger UI.

## Example Request
'''
POST /generate-bullets
{
  "experience": "Led a team of 5 engineers to develop a new feature that increased user engagement by 30%.",
  "job_description": "Looking for a software engineer with strong leadership skills and a track record of delivering impactful features.",
  "style": "xyz"
}
'''
## Retrieval Strategy
- Uses FAISS and sentence-transformers for similarity-based chunk retrieval

- Query rewriting with Gemini LLM to inject relevant context

- Fallback: if retrieval is weak, switch to generic queries using style keywords

## Sample Output
'''
{
  "bullets": [
    "Led a team of 5 engineers to develop a high-impact feature that boosted user engagement by 30%.",
    "Delivered product enhancements aligning with leadership goals outlined in the job description."
  ]
}
'''
## Future Enhancements
 - Feedback-based ranking of generated bullets (RLHF-lite)

 - Real-time ATS score and keyword matching

 - Resume style personalization engine

 - Psychographic matching for hiring manager alignment

## Contributing
Contributions, bug reports, and feedback are welcome. Please open an issue or PR.

## License
MIT License © 2025 Abhinav Singh Chauhan
