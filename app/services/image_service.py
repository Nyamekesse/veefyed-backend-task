"""
Image Service
Handles image upload and storage operations
"""
from fastapi import UploadFile
import logging

from app.utils.validators import validate_image_file
from app.utils.storage import generate_image_id, save_image

logger = logging.getLogger(__name__)


class ImageService:
    """Service for image-related operations"""
    
    @staticmethod
    async def process_upload(file: UploadFile) -> dict:
        """
        Process image upload
        
        Args:
            file: Uploaded image file
            
        Returns:
            Dictionary containing image_id
            
        Raises:
            HTTPException: If validation or storage fails
        """
        logger.info(f"Processing upload: {file.filename}")
        
        # Validate the file
        await validate_image_file(file)
        
        # Generate unique ID
        image_id = generate_image_id()
        logger.info(f"Generated image ID: {image_id}")
        
        # Save the file
        file_path = await save_image(file, image_id)
        logger.info(f"Image saved successfully at: {file_path}")
        
        return {
            "image_id": image_id,
            "filename": file.filename,
            "status": "uploaded"
        }
