from retriever import TranscriptRetriever
from generator import generate_answer

EVAL_CASES = [
    {"question": "How to improve video introductions?", "expected_video": "aprilynne"},
    {"question": "How to improve storytelling?", "expected_video": "hayden"},
    {"question": "How do I start a podcast?", "expected_video": None},
]

def run_generation_eval(top_k=3, use_openai=True):
    retriever = TranscriptRetriever()
    results = []

    for case in EVAL_CASES:
        q = case["question"]
        expected = case["expected_video"]

        retrieved = retriever.search(q, top_k=top_k)
        answer = generate_answer(q, retrieved, use_openai=use_openai)

        passed = False
        if expected is None:
            passed = "couldn't find" in answer.lower()
        else:
            passed = expected in answer

        results.append({
            "question": q,
            "expected": expected,
            "answer": answer,
            "pass": passed
        })
    return results

if __name__ == "__main__":
    eval_results = run_generation_eval()
    print("=== Generation Evaluation ===")
    for r in eval_results:
        status = "PASS" if r["pass"] else "FAIL"
        print(f"Q: {r['question']}")
        print(f"Expected: {r['expected']}")
        print(f"Answer:\n{r['answer']}\n")
        print(status)
        print("="*40)
