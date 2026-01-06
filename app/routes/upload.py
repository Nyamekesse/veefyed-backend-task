"""
Upload Route Handler
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import logging

from app.services.image_service import ImageService
from app.utils.auth import verify_api_key

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    """
    Upload an image for analysis
    
    **Authentication:** Requires X-API-Key header
    
    **Request:**
    - file: Image file (JPEG or PNG, max 5MB)
    
    **Response:**
    - image_id: Unique identifier for the uploaded image
    - filename: Original filename
    - status: Upload status
    
    **Errors:**
    - 400: Invalid file type or size
    - 401: Missing API key
    - 403: Invalid API key
    - 500: Server error
    """
    try:
        logger.info(f"Upload request received for file: {file.filename}")
        
        # Process the upload
        result = await ImageService.process_upload(file)
        
        logger.info(f"Upload successful: {result['image_id']}")
        
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to process image upload"
        )
