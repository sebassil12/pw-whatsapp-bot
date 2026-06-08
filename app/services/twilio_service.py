from twilio.rest import Client
from app.core.config import settings

class TwilioService:
    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )

    def send_whatsapp_message(self, to_number: str, body: str):
        return self.client.messages.create(
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            to=to_number,
            body=body,
        )