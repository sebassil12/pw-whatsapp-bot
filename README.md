# Pawreli WhatsApp Bot

A FastAPI-based WhatsApp bot that receives an image from Twilio WhatsApp, sends it to Google's Gemini API for text extraction, and replies automatically to the user with the extracted information. Twilio's WhatsApp integration is webhook-based, and Google's official Gemini SDK supports Python for multimodal image input workflows.[1][2][3]

## Overview

This project is the first backend prototype for Pawreli's WhatsApp passport flow. A user sends a photo of a vaccine card through WhatsApp, the API receives the webhook from Twilio, the app downloads the image, Gemini extracts visible text and key fields, and Twilio sends the response back to the same WhatsApp number.[4][3][1]

## Tech stack

- **FastAPI** for the webhook API and local development server.[5]
- **Twilio WhatsApp Sandbox/API** for inbound and outbound WhatsApp messaging.[1]
- **Google Gemini API** through the official Python SDK `google-genai` for image understanding and extraction.[2][3]
- **HTTPX** for downloading Twilio media securely over HTTP.[4]
- **Celery + Redis** as the next step for asynchronous background processing when the synchronous prototype is working.[6][7]

## Project structure

```text
pw-whatsapp-bot/
├── app/
│   ├── main.py
│   ├── core/
│   │   └── config.py
│   ├── api/
│   │   └── routes/
│   │       └── whatsapp.py
│   └── services/
│       ├── media_service.py
│       ├── gemini_service.py
│       └── twilio_service.py
├── tests/
├── .env
├── .env.example
├── pyproject.toml
├── README.md
└── uv.lock
```

This layout follows FastAPI's recommended direction for bigger applications by separating routing, configuration, and service logic into clear modules instead of growing a single `main.py` file.[5]

## Requirements

- Python 3.12+
- A Twilio account with WhatsApp Sandbox enabled.[8]
- A Gemini API key from Google AI Studio or the Gemini developer platform.[2]
- `uv` installed for dependency management.[9]
- Optional later: Redis, if asynchronous processing is added with Celery.[7]

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sebassil12/pw-whatsapp-bot.git
cd pw-whatsapp-bot
```

2. Sync dependencies:

```bash
uv sync
```

3. Activate the virtual environment if needed:

```bash
source .venv/bin/activate
```

4. Create the environment file:

```bash
cp .env.example .env
```

## Environment variables

Create a `.env` file with values like these:

```env
GEMINI_API_KEY=your_gemini_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
APP_BASE_URL=https://your-ngrok-url.ngrok-free.app
```

Twilio's WhatsApp Sandbox examples use the sandbox sender `whatsapp:+14155238886` during testing.[8]

## Running locally

Start the FastAPI app with Uvicorn:

```bash
uv run uvicorn app.main:app --reload
```

The API should then be available locally at `http://127.0.0.1:8000` and the interactive docs at `http://127.0.0.1:8000/docs`. FastAPI's standard development workflow uses Uvicorn as the local ASGI server.[10][5]

## Expose the webhook

Twilio needs a public HTTPS URL to send incoming WhatsApp webhooks to your local machine. A common development setup is to expose the local FastAPI server with ngrok and configure the Twilio Sandbox webhook URL to point to `/webhooks/whatsapp`.[11][1]

```bash
ngrok http 8000
```

Then set the Twilio Sandbox webhook to:

```text
https://YOUR-NGROK-URL/webhooks/whatsapp
```

## Current request flow

1. A user sends a vaccine card image to the Twilio WhatsApp Sandbox number.[1]
2. Twilio sends an HTTP POST webhook with fields such as `From`, `MessageSid`, `MediaUrl0`, and `MediaContentType0`.[4]
3. The FastAPI route receives the webhook and validates that media is present.
4. The app downloads the image bytes from the Twilio media URL, typically using Twilio credentials for authenticated access.[4]
5. Gemini receives the prompt and image bytes and extracts visible text from the image.[3]
6. Twilio sends the extracted text back to the same WhatsApp user.[1]

## Example prompt strategy

The current extraction prompt should focus on structured veterinary data instead of generic OCR. Gemini works best when asked to extract visible text and return consistent fields such as pet name, owner name, clinic name, vaccines, and dates.[3]

Suggested prompt shape:

```text
Read this veterinary vaccine card image.
Extract the visible text exactly as written.
Then provide a short structured summary with:
- pet name
- owner name
- clinic name
- vaccines
- dates
If a field is missing, say "not found".
```

## Development roadmap

### Phase 1: Synchronous prototype

- Receive image webhook.
- Download image.
- Send image to Gemini.
- Reply through Twilio.

This phase proves the core Pawreli loop as fast as possible.[1][3]

### Phase 2: Async processing

- Add Celery worker.
- Add Redis broker.
- Return a quick webhook acknowledgment.
- Move Gemini processing into background tasks.

Celery is a better fit than lightweight in-process background execution when retries, queueing, and independent workers are needed.[6][7]

### Phase 3: Production hardening

- Validate Twilio request signatures.[12]
- Add structured Pydantic schemas.[13]
- Add retries, logging, and error handling.
- Add tests for webhook and extraction services.[5]
- Replace free-text output with normalized JSON extraction.

## Suggested VS Code debug targets

Use two common debug entrypoints:

- FastAPI app: `app.main:app`
- Celery app later: `app.core.celery_app:celery_app`

This separation keeps infrastructure concerns out of task modules and makes local debugging more stable as the project grows.[14][7]

## Notes

- Keep webhook handlers thin and move external provider logic into `services/` modules.[5][13]
- Do not duplicate `pyproject.toml` inside `app/`; keep one project root configuration file.[15][16]
- Start with the synchronous path first, then introduce Celery after the integration works end to end.[6][1]

## Next steps

- Add `.env.example`
- Add request signature validation for Twilio.[12]
- Add Celery and Redis.
- Add tests and CI.
- Add structured extraction output for Pawreli passport records.