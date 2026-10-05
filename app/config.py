from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR/".env")

def _env(name, default):
    return os.getenv(name, default)

DATA_DIR = BASE_DIR / "storage"

DB_PATH = DATA_DIR / "documents.db"
CHROMA_PATH = DATA_DIR / "chroma_experiment"
UPLOAD_PATH = DATA_DIR / "uploads"
LOG_PATH = BASE_DIR / "logs"

EMBED_MODEL = _env("EMBED_MODEL","qwen3.7-text-embedding-flash")
CHAT_MODEL = _env("CHAT_MODEL","kimi-k2.6")

COLLECTION_NAME = _env("COLLECTION_NAME","personal_documents")

KIMI_API_KEY = _env("KIMI_API_KEY","")
EMBED_API_KEY = _env("EMBED_API_KEY","")

AI_URL = _env("AI_URL","https://api.moonshot.cn/v1")
EMBED_AI_URL = _env("EMBED_AI_URL","https://maas.qianwenaiapi.com/compatible-mode/v1")

API_KEYS = [k.strip() for k in _env("API_KEYS", "").split(",") if k.strip()]
