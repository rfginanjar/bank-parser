import pytesseract
from PIL import Image

def run_ocr(image_path: str, engine: str) -> str:
    # open image, apply OCR using specified engine
    # return extracted text
    return pytesseract.image_to_string(Image.open(image_path))
