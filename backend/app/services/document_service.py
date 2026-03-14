from fastapi import UploadFile
from pathlib import Path
from app.config import settings
import aiofiles


async def save_file(file: UploadFile, user_id: str) -> str:
    user_dir = Path(settings.STORAGE_PATH) / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    file_path = user_dir / (file.filename or "upload")
    content = await file.read()
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)
    return str(file_path)


async def extract_text(file_path: str, content_type: str) -> str:
    """Extract text from PDF or image. Returns empty string on failure."""
    try:
        if "pdf" in (content_type or ""):
            import pdfplumber
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += (page.extract_text() or "") + "\n"
            return text.strip()
        elif "image" in (content_type or ""):
            import pytesseract
            from PIL import Image
            return pytesseract.image_to_string(Image.open(file_path))
    except Exception:
        pass
    return ""
