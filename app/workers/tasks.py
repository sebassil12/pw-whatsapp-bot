# app/workers/tasks.py
from celery import Celery

celery_app = Celery(
    "pawreli",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_whatsapp_image(self, from_number, message_sid, media_url, media_type):
    # 1) download image
    # 2) send to Gemini
    # 3) format response
    # 4) send WhatsApp reply via Twilio
    return {"ok": True}