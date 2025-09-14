
**Design**


![Arch_Image](https://github.com/user-attachments/assets/abee326f-33c3-4588-a138-90398bec7561)

**Goals**

	•	Build a chatbot that gives YouTube creators advice grounded in transcripts only.
	•	Ensure every answer includes citations with video ID and timestamp.
	•	Keep system simple but production-minded: modular code, Dockerized services, and evaluation harness.


**Architecture**

**Components**

	1.	Preprocessor (preprocessor.py)
	•	Parses transcript files (SRT/WebVTT-style).
	•	Extracts {start_time, end_time, text} entries.

	2.	Chunker (chunk.py)
	•	Groups small subtitle lines into larger segments.
	•	Balances retrieval granularity vs. context size.

	3.	Embedder (embed.py)
	•	Embeds text chunks with all-MiniLM-L6-v2 (SentenceTransformers)
	•	Local + free → reproducible across environments.

	4.	Vector Store (Qdrant)
	•	Stores embeddings + metadata (video_id, timestamps, text).
	•	Supports semantic search + metadata filtering.
	•	Lightweight, production-ready, with REST/gRPC.

	5.	Retriever (retriever.py)
	•	Converts query → embedding.
	•	Searches Qdrant for nearest neighbors.
	•	Supports video_id filtering.

	6.	Generator (generator.py)
	•	Baseline: stitches retrieved chunks + citations.
	•	Optional: uses OpenAI GPT-4o-mini for fluent synthesis (but still grounded).

	7.	FastAPI (main.py, ask.py)
	•	Exposes POST /ask {question, video_id?}.
	•	Returns {question, answer, chunks[]}.

	8.	Evaluation (eval.py, eval_bertscore.py, eval_judge.py)
	•	Retriever Eval → checks grounding + fallback.
	•	BERTScore Eval → quantitative semantic match with transcript.
	•	LLM-as-Judge Eval → qualitative scoring of grounding, citations, clarity.


**Tradeoffs**

	•	Qdrant vs. FAISS vs. Weaviate
	•	Qdrant chosen: lightweight, hybrid search support, metadata filtering.
	•	FAISS too barebones (no metadata, no persistence).
	•	Weaviate heavier, more complex than needed.
	•	Embeddings: MiniLM vs. OpenAI text-embedding-3-large
	•	MiniLM: free, reproducible, small footprint (384-dim).
	•	OpenAI: stronger recall, but paid + external dependency.
	•	For reproducibility → MiniLM is better fit.
	•	Generation: Extractive vs. LLM
	•	Baseline: extractive → guarantees grounding.
	•	OpenAI option: more fluent → risk of hallucination but nicer answers.
	•	Both supported, user can choose.
	•	Chunking Strategy
	•	Simple fixed-size grouping (3–5 lines).
	•	Future: semantic segmentation (e.g. sentence-level embeddings).


**Scaling & Extensibility**

	•	More transcripts → just rerun ingestion script.
	•	Hybrid retrieval → add keyword BM25 fallback (Qdrant supports this).
	•	Frontend → React or Streamlit can easily call FastAPI.
	•	Analytics → track which chunks get retrieved most often.


**Evaluation Plan**

	•	Retriever: Hits@k, grounding checks (expected video retrieved).
	•	Generator:
	•	Schema Test → citations always present.
	•	BERTScore → semantic overlap with reference transcript.
	•	LLM-as-Judge → qualitative evaluation of grounding, clarity, citations.
	•	Fallback: gracefully decline when no transcript coverage.


