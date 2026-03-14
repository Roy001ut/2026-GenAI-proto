from fastapi import UploadFile
from PIL import Image
import pytesseract
import pdfplumber
from pathlib import Path
from app.config import settings
import aiofiles
from typing import Optional


class DocumentService:
    @staticmethod
    async def save_file(file: UploadFile, user_id: str) -> str:
        """Save uploaded file to disk"""
        user_dir = Path(settings.STORAGE_PATH) / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        file_path = user_dir / file.filename
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)

        return str(file_path)

    @staticmethod
    async def extract_text(file_path: str, content_type: str) -> str:
        """Extract text from PDF or image"""
        if "pdf" in content_type:
            return DocumentService._extract_from_pdf(file_path)
        elif "image" in content_type:
            return DocumentService._extract_from_image(file_path)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting from PDF: {e}")
        return text

    @staticmethod
    def _extract_from_image(file_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error extracting from image: {e}")
            return ""
