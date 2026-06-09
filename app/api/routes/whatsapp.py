from fastapi import APIRouter, Form, Response
from app.core.config import settings
from app.services.media_service import MediaService
from app.services.gemini_service import GeminiService
from app.services.twilio_service import TwilioService
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()

@router.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    MessageSid: str = Form(...),
    MediaUrl0: str | None = Form(None),
    MediaContentType0: str | None = Form(None),
    Body: str | None = Form(None),
):
    twilio = TwilioService()

    if not MediaUrl0 or not MediaContentType0:
        twiml = MessagingResponse()
        twiml.message("Please send a photo of the vaccine card.")
        return Response(content=str(twiml), media_type="application/xml")


    image_bytes = MediaService.download_bytes(
        media_url=MediaUrl0,
        account_sid=settings.TWILIO_ACCOUNT_SID,
        auth_token=settings.TWILIO_AUTH_TOKEN,
    )

    extracted = GeminiService().extract_text_from_image(
        image_bytes=image_bytes,
        mime_type=MediaContentType0,
    )

    twilio.send_whatsapp_message(
        to_number=From,
        body=extracted[:1500]
    )

    return {"status": "processed", "message_sid": MessageSid}