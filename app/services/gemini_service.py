from google import genai
from google.genai import types
from app.core.config import settings

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def extract_text_from_image(self, image_bytes: bytes, mime_type: str) -> str:
        prompt = """
        Read this veterinary vaccine card image.
        Extract the visible text exactly as written.
        Then provide a short structured summary with:
        - pet name
        - owner name
        - clinic name
        - vaccines
        - dates
        If a field is missing, say 'not found'.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            ],
        )
        return response.text or "I could not extract text from the image."