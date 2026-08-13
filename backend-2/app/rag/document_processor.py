from fastapi import UploadFile
from pypdf import PdfReader
from io import BytesIO
from PIL import Image
import pytesseract


async def process_document(file: UploadFile) -> str:
    
    if file.content_type == "text/plain":
        return await process_text(file)

    elif file.content_type == "application/pdf":
        return await process_pdf(file)

    elif file.content_type.startswith("image/"):
        return await process_image(file)

    else:
        raise ValueError(
            "Unsupported file type. Please upload a TXT, PDF, or image file."
        )


async def process_text(file: UploadFile) -> str:
    content = await file.read()
    return content.decode("utf-8")


async def process_pdf(file: UploadFile) -> str:
    content = await file.read()
    pdf = PdfReader(BytesIO(content))
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


async def process_image(file: UploadFile) -> str:
    content = await file.read()
    # Read the uploaded image as bytes

    image = Image.open(BytesIO(content))
    # BytesIO wraps the bytes as a file-like object so Pillow can open the image

    text = pytesseract.image_to_string(image)
    # Tesseract OCR analyzes the image pixels and extracts recognizable text

    return text