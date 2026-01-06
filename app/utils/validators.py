"""
Validation Utilities
"""

from fastapi import UploadFile, HTTPException
from pathlib import Path
import logging

from app.config import settings

logger = logging.getLogger(__name__)


def validate_file_extension(filename: str) -> None:
    """
    Validate file extension

    Args:
        filename: Name of the file to validate

    Raises:
        HTTPException: If file extension is not allowed
    """
    file_ext = Path(filename).suffix.lower()

    if file_ext not in settings.ALLOWED_EXTENSIONS:
        allowed = ", ".join(settings.ALLOWED_EXTENSIONS)
        logger.warning(f"Invalid file extension attempted: {file_ext}")
        raise HTTPException(
            status_code=400, detail=f"Invalid file type. Allowed types: {allowed}"
        )


async def validate_file_size(file: UploadFile) -> None:
    """
    Validate file size

    Args:
        file: Uploaded file to validate

    Raises:
        HTTPException: If file size exceeds maximum
    """
    contents = await file.read()
    file_size = len(contents)

    await file.seek(0)

    if file_size > settings.MAX_FILE_SIZE:
        max_size_mb = settings.MAX_FILE_SIZE / (1024 * 1024)
        logger.warning(f"File size {file_size} exceeds limit {settings.MAX_FILE_SIZE}")
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {max_size_mb}MB",
        )

    logger.info(f"File size validated: {file_size} bytes")


async def validate_image_file(file: UploadFile) -> None:
    """
    Validate uploaded image file

    Args:
        file: Uploaded file to validate

    Raises:
        HTTPException: If validation fails
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    validate_file_extension(file.filename)

    await validate_file_size(file)

    logger.info(f"File validation passed: {file.filename}")
