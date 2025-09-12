from typing import List, Dict, Optional
from dotenv import load_dotenv

import os

load_dotenv()

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    client = None

def generate_answer(
    question: str,
    retrieved: List[Dict],
    use_openai: bool = False,
    model: str = "gpt-4o-mini"
) -> str:
    """
    Generate answer with citations.
    If use_openai=True, call OpenAI for synthesis.
    Otherwise, return simple stitched answer.
    """
    if not retrieved:
        return "Sorry, I couldn't find relevant information in the transcripts."

    context_chunks = []
    for r in retrieved:
        citation = f'[source: "{r["video_id"]}" t={r["start_time"]}-{r["end_time"]}]'
        context_chunks.append(f"{r['text']} {citation}")

    context_text = "\n".join(context_chunks)

    if use_openai and client:
        prompt = f"""
You are a helpful assistant. 
Answer the following question based only on the transcript excerpts.

Question: {question}

Transcript excerpts:
{context_text}

Rules:
- Only use the provided excerpts.
- Every claim must include at least one citation in the given format.
- If the answer is not in the excerpts, say so.
"""
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You ground answers in transcripts with citations."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    # Fallback: simple stitched answer
    return "\n".join(f"- {c}" for c in context_chunks)
