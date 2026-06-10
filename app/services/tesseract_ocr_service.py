# app/services/tesseract_ocr_service.py
import io
import pytesseract
from PIL import Image, ImageOps

class TesseractOCRService:
    def extract_text_from_image(self, image_bytes: bytes, mime_type: str | None = None) -> str:
        image = Image.open(io.BytesIO(image_bytes))

        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB")

        image = ImageOps.exif_transpose(image)
        image = ImageOps.grayscale(image)

        text = pytesseract.image_to_string(image, lang="eng+spa")

        text = text.strip()
        if not text:
            return "I couldn't read clear text from that image. Please send a sharper, well-lit photo."

        return text