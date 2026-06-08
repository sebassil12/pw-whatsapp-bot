from fastapi import FastAPI
from app.api.routes.whatsapp import router as whatsapp_router

app = FastAPI(title="Pawreli WhatsApp Bot")

app.include_router(whatsapp_router, prefix="/webhooks")