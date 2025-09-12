def chunk_transcript(entries, chunk_size=5):
    """
    Group transcript entries into larger chunks.
    """
    chunks = []
    for i in range(0, len(entries), chunk_size):
        group = entries[i:i+chunk_size]
        if not group:
            continue
        text = " ".join([g["text"] for g in group])
        chunks.append({
            "video_id": "unknown",  # will be overridden in ingestion
            "text": text,
            "start_time": group[0]["start_time"],
            "end_time": group[-1]["end_time"]
        })
    return chunks
