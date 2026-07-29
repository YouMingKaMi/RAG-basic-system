def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    chunk = []
    step = chunk_size - overlap
    for start in range(0, len(text), step):
        chunk.append(text[start: start + chunk_size])
    return chunk

if __name__ == "__main__":
    text = "zxcvbnmasdfghjklqwertyuioop"
    print(chunk_text(text))