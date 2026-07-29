from pathlib import Path

def text_parser(stored_path: str) -> str:
    path = Path(stored_path)
    content_str = path.read_text("utf-8")

    return content_str

if __name__ == "__main__":
    print(text_parser("storage/uploads/42b9e965bf474f458f589c0fdc2b9681.md"))