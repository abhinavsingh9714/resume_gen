from retriever import KnowledgeBaseRetriever

class PromptBuilder:
    def __init__(self):
        self.retriever = KnowledgeBaseRetriever()

    def build_prompt(self, experience: str, job_description: str = "", style: str = "metrics"):
        # Step 1: Retrieve relevant knowledge base chunks
        query = "How to write effective resume bullet points in {} style".format(style)
        kb_chunks = self.retriever.retrieve(query, top_k=3)

        # Step 2: Combine retrieved content
        guidance_section = "\n\n".join([f"• {chunk['content']}" for chunk in kb_chunks])
        
        # Step 3: Format final prompt
        prompt = f"""
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

        return prompt