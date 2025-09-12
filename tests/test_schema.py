from src.utils.generator import generate_answer

def test_answer_contains_citation():
    retrieved = [{
        "video_id": "aprilynne",
        "text": "Use bold, high-contrast thumbnails.",
        "start_time": "00:10:00",
        "end_time": "00:10:05",
        "score": 0.92
    }]
    ans = generate_answer("How to improve CTR?", retrieved)
    assert "[source:" in ans
    assert "aprilynne" in ans
