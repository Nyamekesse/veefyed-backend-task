"""
Analysis Route Handler
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import logging

from app.services.analysis_service import AnalysisService
from app.utils.auth import verify_api_key

logger = logging.getLogger(__name__)

router = APIRouter()


class AnalyzeRequest(BaseModel):
    """Request model for image analysis"""
    image_id: str
    
    class Config:
        schema_extra = {
            "example": {
                "image_id": "abc123-def456-ghi789"
            }
        }


@router.post("/analyze")
async def analyze_image(
    request: AnalyzeRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze an uploaded image
    
    **Authentication:** Requires X-API-Key header
    
    **Request:**
    - image_id: Unique identifier of the uploaded image
    
    **Response:**
    - image_id: Image identifier
    - skin_type: Detected skin type
    - issues: List of detected skin issues
    - confidence: Confidence score (0-1)
    
    **Errors:**
    - 400: Invalid request
    - 401: Missing API key
    - 403: Invalid API key
    - 404: Image not found
    - 500: Server error
    """
    try:
        logger.info(f"Analysis request received for image: {request.image_id}")
        
        if not request.image_id or not request.image_id.strip():
            raise HTTPException(
                status_code=400,
                detail="image_id is required and cannot be empty"
            )
        
        # Perform analysis
        result = await AnalysisService.analyze_image(request.image_id)
        
        logger.info(f"Analysis successful for: {request.image_id}")
        
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze image"
        )
