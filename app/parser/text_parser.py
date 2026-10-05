from pathlib import Path

def text_parser(stored_path: str) -> str:
    path = Path(stored_path)
    content_str = path.read_text("utf-8")

    return content_str
