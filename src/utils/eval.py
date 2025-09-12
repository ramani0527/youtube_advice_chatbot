from retriever import TranscriptRetriever
from generator import generate_answer

EVAL_CASES = [
    {"question": "How to improve video introductions?", "expected_video": "aprilynne"},
    {"question": "How to improve storytelling?", "expected_video": "hayden"},
    {"question": "How do I start a podcast?", "expected_video": None},
]

def run_eval(top_k=3):
    retriever = TranscriptRetriever()
    results = []

    for case in EVAL_CASES:
        q = case["question"]
        expected = case["expected_video"]

        retrieved = retriever.search(q, top_k=top_k)
        answer = generate_answer(q, retrieved)

        passed = False
        if expected is None:
            passed = "couldn't find" in answer.lower()
        else:
            vids = [r["video_id"] for r in retrieved]
            passed = expected in vids

        results.append({
            "question": q,
            "expected": expected,
            "retrieved_videos": [r["video_id"] for r in retrieved],
            "answer": answer,
            "pass": passed
        })
    return results

if __name__ == "__main__":
    eval_results = run_eval()
    print("=== Retriever Evaluation ===")
    for r in eval_results:
        status = "PASS" if r["pass"] else "FAIL"
        print(f"Q: {r['question']}")
        print(f"Expected: {r['expected']} | Retrieved: {r['retrieved_videos']}")
        print(f"Answer: {r['answer'][:120]}...")
        print(status)
        print()
