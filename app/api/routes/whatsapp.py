from fastapi import APIRouter, Form, Response
from twilio.twiml.messaging_response import MessagingResponse

from app.core.config import settings
from app.services.media_service import MediaService
from app.services.tesseract_ocr_service import TesseractOCRService

router = APIRouter()

@router.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    MessageSid: str = Form(...),
    MediaUrl0: str | None = Form(None),
    MediaContentType0: str | None = Form(None),
    Body: str | None = Form(None),
):
    if not MediaUrl0 or not MediaContentType0:
        twiml = MessagingResponse()
        twiml.message("Please send a photo of the vaccine card.")
        return Response(content=str(twiml), media_type="application/xml")

    try:
        image_bytes = MediaService.download_bytes(
            media_url=MediaUrl0,
            account_sid=settings.TWILIO_ACCOUNT_SID,
            auth_token=settings.TWILIO_AUTH_TOKEN,
        )

        extracted = TesseractOCRService().extract_text_from_image(
            image_bytes=image_bytes,
            mime_type=MediaContentType0,
        )

        cleaned = " ".join(extracted.split())
        reply = cleaned[:1400] if cleaned else "I couldn't read the card clearly. Please send a sharper photo."

        twiml = MessagingResponse()
        twiml.message(reply)
        return Response(content=str(twiml), media_type="application/xml")

    except Exception:
        twiml = MessagingResponse()
        twiml.message("I couldn't process that image. Please try again with a clearer photo.")
        return Response(content=str(twiml), media_type="application/xml")