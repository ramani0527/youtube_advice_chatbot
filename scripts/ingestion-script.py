import sys, os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

sys.path.append(os.path.abspath("./src"))
from utils.chunk import chunk_transcript
from utils.preprocessor import load_transcript

COLLECTION_NAME = "transcripts"
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")

def create_collection(client):
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

def ingest_file(file_path, video_id, model, client):
    print(f"Ingesting {file_path} ...")
    entries = load_transcript(file_path)
    chunks = chunk_transcript(entries, chunk_size=3)

    # attach video_id
    for c in chunks:
        c["video_id"] = video_id

    vectors = model.encode([c["text"] for c in chunks]).tolist()
    client.upload_collection(
        collection_name=COLLECTION_NAME,
        vectors=vectors,
        payload=chunks,
        ids=None,
        batch_size=32,
    )
    print(f"Inserted {len(chunks)} chunks for {video_id}")

if __name__ == "__main__":
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    client = QdrantClient(url=QDRANT_URL)
    create_collection(client)

    transcripts = {
        "aprilynne": "transcripts/aprilynne.txt",
        "hayden": "transcripts/hayden.txt"
    }

    for video_id, path in transcripts.items():
        ingest_file(path, video_id, model, client)

