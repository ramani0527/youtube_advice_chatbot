import re

def load_transcript(path):
    """
    Load transcript text file in WebVTT/SRT-like format.
    Returns list of dicts with {start_time, end_time, text}.
    """
    entries = []
    with open(path, "r") as f:
        raw = f.read().strip()

    blocks = re.split(r"\n\s*\n", raw)
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            ts_line = lines[1]
            text = " ".join(lines[2:])
            start, end = ts_line.split("-->")
            entries.append({
                "start_time": start.strip(),
                "end_time": end.strip(),
                "text": text.strip()
            })
    return entries
