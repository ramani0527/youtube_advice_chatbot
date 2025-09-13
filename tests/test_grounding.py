from utils.generator import generate_answer

def test_grounding_video_specific():
    retrieved = [{
        "video_id": "hayden",
        "text": "Good storytelling keeps viewers watching longer.",
        "start_time": "00:20:00",
        "end_time": "00:20:10",
        "score": 0.88
    }]
    ans = generate_answer("How to keep viewers engaged?", retrieved)
    assert "hayden" in ans
    assert "aprilynne" not in ans
