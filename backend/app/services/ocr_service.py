import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
from typing import Optional

# Ensure tesseract is in PATH or set explicitly
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_tesseract>'


def run_ocr_on_image(image_path: str, lang: str = "eng") -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text


def run_ocr_on_pdf(pdf_path: str, lang: str = "eng") -> str:
    images = convert_from_path(pdf_path)
    texts = []
    for img in images:
        text = pytesseract.image_to_string(img, lang=lang)
        texts.append(text)
    return "\n".join(texts)


def run_ocr(file_path: str, engine: str = "tesseract", lang: str = "eng") -> str:
    # For MVP, only tesseract engine is supported
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return run_ocr_on_pdf(file_path, lang)
    else:
        return run_ocr_on_image(file_path, lang)
