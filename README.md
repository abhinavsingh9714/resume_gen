# Resume Bullet Generator

A FastAPI-powered service that generates ATS-optimized, quantified, and job-tailored resume bullet points. This tool leverages a powerful hybrid approach, combining semantic search over a curated knowledge base with advanced rewriting and generation capabilities from Google's Gemini models.

---

## Key Features

* **High-Impact Bullet Generation**: Creates compelling bullet points using established professional formats like XYZ and STAR, or your own custom style.
* **Semantic Knowledge Retrieval**: Utilizes a FAISS index and Sentence Transformers to find the most relevant examples and advice from a built-in knowledge base of resume guides.
* **Gemini-Powered Intelligence**:
    * **Query Rewriting**: Enhances user input to create smarter, context-aware prompts for the language model.
    * **LLM Generation**: Employs Gemini to generate high-quality bullet points, with built-in post-processing and fallback logic for reliability.
* **Production-Ready**: Features a modular design, comprehensive `pytest` test coverage, and straightforward deployment.

---

## Project Structure

``` text
resume_gen/
├── kb_chunks/          # Chunked knowledge base (.jsonl)
├── kb_index/           # FAISS index files
├── knowledge_base/     # Raw .txt resume writing guides
├── src/
│   ├── config.py       # Configuration paths and constants
│   ├── embed_and_store.py # Embedding and FAISS indexing script
│   ├── retriever.py    # FAISS and transformer-based retriever
│   ├── query_rewriter.py # Gemini-based query enhancer
│   ├── prompt_builder.py # Prompt construction logic
│   ├── llm.py          # Gemini LLM integration and response parsing
│   ├── main.py         # FastAPI server
│   └── feedback.py     # (Optional) User feedback tracking
├── tests/              # Unit tests with pytest
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the Repository and Set Up the Environment

``` bash
git clone [https://github.com/yourname/resume-gen.git](https://github.com/yourname/resume-gen.git)
cd resume-gen
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a .env file in the project's root directory and add your Gemini API key:

``` bash
GEMINI_API_KEY="your_google_generative_ai_key"
GEMINI_MODEL="gemini-pro"
```

### 3. Build the Knowledge Base Index

This script reads the guides, computes sentence embeddings, and builds the FAISS index for retrieval.

``` bash
python resume_gen/src/embed_and_store.py
```

### 4. Run the FastAPI Server

``` bash
uvicorn resume_gen/src/main:app --reload
```

Once running, you can access the interactive API documentation at http://localhost:8000/docs.

## API Usage

### Example Request

Send a POST request to the /generate-bullets endpoint:

``` json
{
  "experience": "Led a team of 5 engineers to develop a new feature that increased user engagement by 30%.",
  "job_description": "Looking for a software engineer with strong leadership skills and a track record of delivering impactful features.",
  "style": "xyz"
}
```

### Example Response

``` json
{
  "bullets": [
    "Led a 5-person engineering team to develop and launch a new feature, boosting user engagement by 30%.",
    "Delivered a key product enhancement that directly aligned with business goals for leadership and feature impact."
  ]
}
```

## Core Retrieval Strategy

The service employs a multi-step process to generate relevant results:

1. The user's input experience is rewritten by Gemini to be more descriptive and context-rich.
2. The rewritten query is used to retrieve the most semantically similar chunks from the FAISS knowledge base.
3. The retrieved chunks and the original user input are used to build a final, comprehensive prompt for Gemini.
4. If the initial retrieval from the knowledge base is weak, the system falls back to a generic prompt using only the user's input and requested style to ensure a reliable response.

## Future Enhancements

- ***Feedback-Based Ranking***: Implement a simple RLHF-style system to rank and improve generated bullets based on user feedback.
- ***Real-Time ATS Score***: Integrate a feature to provide an estimated ATS score and keyword match analysis.
- ***Personalization Engine***: Allow users to fine-tune the generation style based on their preferences.

##Contributing

Contributions, bug reports, and feedback are highly welcome! Please feel free to open an issue or a pull request on the GitHub repository.

## License
This project is licensed under the MIT License.

© 2025 Abhinav Singh Chauhan. 