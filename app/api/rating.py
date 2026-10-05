from fastapi import APIRouter, Depends
from app.schemas.rating_schema import RatingRequest,RatingResponse
from app.services.rating_service import rating_process
from app.api.deps import require_api_key

router = APIRouter(prefix="/rating",tags=["rating"], dependencies=[Depends(require_api_key)],)

@router.post("/",response_model=RatingResponse)
def rating(request: RatingRequest):
    rating_process(request.message_id, request.feedback, request.content)
    return RatingResponse(message_id=request.message_id, status="Success")
