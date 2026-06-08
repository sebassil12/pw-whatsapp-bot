# app/main.py
from fastapi import FastAPI, Form
from app.workers.tasks import process_whatsapp_image

app = FastAPI()

@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    MessageSid: str = Form(...),
    MediaUrl0: str | None = Form(None),
    MediaContentType0: str | None = Form(None),
    Body: str | None = Form(None),
):
    if MediaUrl0 and MediaContentType0 and MediaContentType0.startswith("image/"):
        process_whatsapp_image.delay(From, MessageSid, MediaUrl0, MediaContentType0)
        return {"status": "queued"}

    return {"status": "ignored", "reason": "no image"}