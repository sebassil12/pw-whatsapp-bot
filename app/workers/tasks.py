from app.core.celery_app import celery_app
from app.services.extraction_service import ExtractionService

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_whatsapp_image(self, from_number: str, media_url: str, media_type: str, message_sid: str):
    ExtractionService().process(
        from_number=from_number,
        media_url=media_url,
        media_type=media_type,
        message_sid=message_sid,
    )