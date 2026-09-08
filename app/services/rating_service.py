from app.repositories.document_repository import add_rating, rating_exists, update_rating, message_exists
from app.exceptions import MessageNotFoundError
import logging

logger = logging.getLogger(__name__)

def rating_process(message_id: int, rating: int, rating_content: str):
    if not message_exists(message_id):
        raise MessageNotFoundError("The message_id can not be found!!")
    
    if rating_exists(message_id):
        update_rating(message_id, rating, rating_content)
    else:
        add_rating(message_id, rating, rating_content)

    if rating == 0:
        logger.warning(f"Negative rating on message{message_id}")


