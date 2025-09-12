from retriever import TranscriptRetriever
from generator import generate_answer
import bert_score

EVAL_CASES = [
    {"question": "How to improve video introductions?", "expected_video": "aprilynne"},
    {"question": "How to improve storytelling?", "expected_video": "hayden"},
]

def run_bertscore_eval(top_k=3, use_openai=True):
    retriever = TranscriptRetriever()
    results = []

    for case in EVAL_CASES:
        q = case["question"]
        expected = case["expected_video"]

        retrieved = retriever.search(q, top_k=top_k, video_id=expected)
        references = [r["text"] for r in retrieved] or [""]

        answer = generate_answer(q, retrieved, use_openai=use_openai)

        P, R, F1 = bert_score.score(
            [answer],
            [" ".join(references)],
            lang="en",
            verbose=False
        )

        results.append({
            "question": q,
            "expected": expected,
            "answer": answer,
            "precision": P.tolist()[0],
            "recall": R.tolist()[0],
            "f1": F1.tolist()[0],
        })
    return results

if __name__ == "__main__":
    results = run_bertscore_eval()
    print("=== BERTScore Evaluation ===")
    for r in results:
        print(f"Q: {r['question']}")
        print(f"Expected: {r['expected']}")
        print(f"Answer: {r['answer'][:100]}...")
        print(f"Scores → Precision: {r['precision']:.3f}, Recall: {r['recall']:.3f}, F1: {r['f1']:.3f}")
        print("="*50)
