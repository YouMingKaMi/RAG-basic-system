from fastapi import FastAPI 
from app.api.documents import router as documents_router
from app.api.search import router as search_router
from app.api.rating import router as rating_router
from app.api.exception_handlers import register_exception_handlers
from app.logging_cofig import setup_logging

app = FastAPI()

app.include_router(documents_router)
app.include_router(search_router)
app.include_router(rating_router)

register_exception_handlers(app)

setup_logging()

@app.get("/")
def read_root():
    return {"message": "RAG Knowledge Base API is running"}