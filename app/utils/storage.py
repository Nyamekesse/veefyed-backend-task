"""
Storage Utilities
"""

import uuid
import aiofiles
from pathlib import Path
from fastapi import UploadFile
import logging

from app.config import settings

logger = logging.getLogger(__name__)


def generate_image_id() -> str:
    """
    Generate a unique image ID

    Returns:
        Unique identifier string
    """
    return str(uuid.uuid4())


def get_file_path(image_id: str, extension: str) -> Path:
    """
    Get full file path for an image

    Args:
        image_id: Unique image identifier
        extension: File extension (e.g., '.jpg')

    Returns:
        Full path to the file
    """
    filename = f"{image_id}{extension}"
    return settings.UPLOAD_DIR / filename


async def save_image(file: UploadFile, image_id: str) -> Path:
    """
    Save uploaded image to local storage

    Args:
        file: Uploaded file
        image_id: Unique identifier for the image

    Returns:
        Path where the file was saved
    """
    # Get file extension
    if not file.filename:
        raise ValueError("Uploaded file must have a filename")
    extension = Path(file.filename).suffix.lower()

    # Determine save path
    file_path = get_file_path(image_id, extension)

    # Save file
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    logger.info(f"Image saved: {file_path}")
    return file_path


def image_exists(image_id: str) -> bool:
    """
    Check if an image exists for the given ID

    Args:
        image_id: Image identifier to check

    Returns:
        True if image exists, False otherwise
    """
    # Check for common extensions
    for ext in settings.ALLOWED_EXTENSIONS:
        file_path = get_file_path(image_id, ext)
        if file_path.exists():
            logger.info(f"Image found: {file_path}")
            return True

    logger.warning(f"Image not found for ID: {image_id}")
    return False


def get_existing_image_path(image_id: str) -> Path:
    """
    Get the path of an existing image

    Args:
        image_id: Image identifier

    Returns:
        Path to the image file

    Raises:
        FileNotFoundError: If image doesn't exist
    """
    for ext in settings.ALLOWED_EXTENSIONS:
        file_path = get_file_path(image_id, ext)
        if file_path.exists():
            return file_path

    raise FileNotFoundError(f"Image not found: {image_id}")
