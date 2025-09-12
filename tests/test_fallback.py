from src.utils.generator import generate_answer

def test_fallback_graceful():
    retrieved = []
    ans = generate_answer("How do I start a podcast?", retrieved)
    assert "couldn't find" in ans.lower()
    