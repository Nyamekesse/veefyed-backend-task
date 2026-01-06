"""
Authentication Utilities
"""

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
import logging

from app.config import settings

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify API key from request header

    Args:
        api_key: API key from request header

    Returns:
        The validated API key

    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not api_key:
        logger.warning("API key missing from request")
        raise HTTPException(
            status_code=401, detail="API key is required. Include 'X-API-Key' header."
        )

    if api_key != settings.API_KEY:
        logger.warning(f"Invalid API key attempted: {api_key[:8]}...")
        raise HTTPException(status_code=403, detail="Invalid API key")

    logger.info("API key validated successfully")
    return api_key
