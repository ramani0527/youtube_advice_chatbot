import os
from openai import OpenAI
from utils.retriever import TranscriptRetriever
from utils.generator import generate_answer

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EVAL_CASES = [
    {"question": "How to improve video introductions?", "expected_video": "aprilynne"},
    {"question": "How to improve storytelling?", "expected_video": "hayden"},
    {"question": "How do I start a podcast?", "expected_video": None},
]

def judge_answer(question, answer, expected_video):
    prompt = f"""
You are a strict evaluator.
Check the answer against these rules:

1. The answer must cite transcript sources in format [source: "<video_id>" t=..–..].
2. Every claim must be grounded in the transcripts.
3. If expected_video is not None, it must appear in the answer.
4. If expected_video is None, the answer must gracefully decline.

Question: {question}
Expected Video: {expected_video}
Answer:
{answer}

Return JSON with:
- groundedness: 1-5
- citation: 1-5
- relevance: 1-5
- pass: true/false
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def run_judge_eval():
    retriever = TranscriptRetriever()
    results = []

    for case in EVAL_CASES:
        q = case["question"]
        expected = case["expected_video"]

        retrieved = retriever.search(q, top_k=3)
        answer = generate_answer(q, retrieved, use_openai=True)

        judgment = judge_answer(q, answer, expected)
        results.append({"question": q, "answer": answer, "judgment": judgment})
    return results

if __name__ == "__main__":
    eval_results = run_judge_eval()
    print("=== LLM-as-Judge Evaluation ===")
    for r in eval_results:
        print(f"Q: {r['question']}")
        print(f"Answer:\n{r['answer']}\n")
        print(f"Judgment: {r['judgment']}")
        print("="*40)
