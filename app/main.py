from fastapi import FastAPI # type:ignore
from app.api.documents import router as documents_router
from app.api.search import router as search_router

app = FastAPI()

app.include_router(documents_router)
app.include_router(search_router)

@app.get("/")
def read_root():
    return {"message": "RAG Knowledge Base API is running"}