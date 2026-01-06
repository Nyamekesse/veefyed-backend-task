"""
Application Configuration
"""

import os
from pathlib import Path


class Settings:
    """Application settings"""

    # API Settings
    API_KEY: str = os.getenv("API_KEY", "veefyed-UV9tbAcqbFpk")

    # File Upload Settings
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png"}
    UPLOAD_DIR: Path = Path("uploads")

    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    def __init__(self):
        # Create upload directory if it doesn't exist
        self.UPLOAD_DIR.mkdir(exist_ok=True)


settings = Settings()
