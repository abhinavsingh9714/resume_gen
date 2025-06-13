from src.retriever import KnowledgeBaseRetriever
from src.query_rewriter import QueryRewriter

class PromptBuilder:
    def __init__(self, use_gemini: bool = True):
        self.retriever = KnowledgeBaseRetriever()
        self.use_gemini = use_gemini
        self.rewriter = QueryRewriter() if use_gemini else None

    def build_prompt(self, experience: str, job_description: str = "", style: str = "xyz") -> str:
        # Step 1: Create query
        if self.use_gemini:
            query = self.rewriter.rewrite(experience, job_description, style)
        else:
            query = self._build_fallback_query(experience, job_description, style)
        # print(f"Query for knowledge base: {query}")
        # Step 2: Retrieve chunks
        kb_chunks = self.retriever.retrieve(query, top_k=3)

        # Step 3: Fallback if weak results
        if not kb_chunks or all(len(c["content"].strip()) < 50 for c in kb_chunks):
            fallback_query = f"Resume bullet writing in {style.upper()} style"
            kb_chunks = self.retriever.retrieve(fallback_query, top_k=3)

        guidance_section = "\n\n".join([f"• {chunk['content']}" for chunk in kb_chunks])
        # print(f'**************generated guidance section: {guidance_section}')
        # Step 4: Final prompt
        return f"""
You are a professional resume writer helping candidates craft impactful, ATS-optimized resume bullet points.

Instructions:
- Use the {style.upper()} style (e.g., STAR, XYZ) for the bullet points.
- Focus on quantifiable outcomes, action verbs, and clarity.
- Each bullet should be a single, clear sentence.
- Do not invent fake results — only use provided information.

Knowledge base guidance:
{guidance_section}

Candidate Experience:
{experience}

Job Description:
{job_description}

Now write 2 high-impact bullet points that match the job description and showcase the candidate’s achievements.
""".strip()

    def _build_fallback_query(self, experience: str, job_description: str, style: str) -> str:
        key_terms = self._extract_key_terms(experience + " " + job_description)
        return f"How to write effective resume bullet points in {style.upper()} style using: {', '.join(key_terms)}"

    def _extract_key_terms(self, text: str, max_terms: int = 8) -> list:
        # Naive keyword extraction (can be replaced by spaCy, YAKE, RAKE etc.)
        import re
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        common = {"with", "that", "have", "your", "just", "from", "this", "these", "those", "using", "skills"}
        keywords = [w for w in words if w not in common]
        return list(dict.fromkeys(keywords))[:max_terms]  # dedup + cap

if __name__ == "__main__":
    builder = PromptBuilder(use_gemini=True)  # Set to True to use Gemini
    experience = "Led a team of 5 engineers to develop a new feature that increased user engagement by 30%."
    job_description = "Looking for a software engineer with strong leadership skills and a track record of delivering impactful features."
    prompt = builder.build_prompt(experience, job_description, style="xyz")
    print("Generated Prompt:\n")
    print(prompt)