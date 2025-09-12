from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import os

class TranscriptRetriever:
    def __init__(
        self,
        collection_name: str = "transcripts",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        qdrant_url: str = "http://qdrant:6333"
    ):
        self.collection = collection_name
        self.client = QdrantClient(url=qdrant_url)
        self.model = SentenceTransformer(model_name)

    def search(
        self,
        query: str,
        top_k: int = 5,
        video_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query_vector = self.model.encode(query).tolist()

        q_filter = None
        if video_id:
            q_filter = Filter(
                must=[
                    FieldCondition(
                        key="video_id",
                        match=MatchValue(value=video_id)
                    )
                ]
            )

        search_result = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            query_filter=q_filter,
            limit=top_k
        )

        results = []
        for hit in search_result:
            payload = hit.payload
            results.append({
                "video_id": payload.get("video_id"),
                "text": payload.get("text"),
                "start_time": payload.get("start_time"),
                "end_time": payload.get("end_time"),
                "score": hit.score
            })
        return results
