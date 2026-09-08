from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import InvalidUploadError, DocumentProcessError, DocumentNotFoundError, MessageNotFoundError

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(InvalidUploadError)
    def invalid_upload_handler(request: Request, error: InvalidUploadError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(error)
            }
        )

    @app.exception_handler(DocumentProcessError)
    def document_process_handler(request: Request, error: DocumentProcessError):
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(error)
            }
        )

    @app.exception_handler(DocumentNotFoundError)
    def docuemnt_not_found_handler(request: Request, error: DocumentNotFoundError):
        return JSONResponse(
            status_code=404,
            content = {
                "detail": str(error)
            }
        )

    @app.exception_handler(MessageNotFoundError)
    def message_not_found_handler(request: Request, error: MessageNotFoundError):
        return JSONResponse(
            status_code=404,
            content = {
                "detail":str(error)
            }
        )
    