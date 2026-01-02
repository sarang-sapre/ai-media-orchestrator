"""
Configuration management for AI Media Orchestrator.
Loads settings from environment variables.
"""

import os
from pathlib import Path
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""
    
    # Version
    VERSION = "0.1.0"
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent.parent
    ASSETS_DIR = Path(__file__).parent / "assets"
    AUDIO_DIR = ASSETS_DIR / "audio"
    VIDEO_DIR = ASSETS_DIR / "video"
    OUTPUT_DIR = ASSETS_DIR / "output"
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Voice Generation
    VOICE_MODEL: str = os.getenv("VOICE_MODEL", "tts-1")
    VOICE_NAME: str = os.getenv("VOICE_NAME", "alloy")
    
    # Video Settings
    VIDEO_RESOLUTION: str = os.getenv("VIDEO_RESOLUTION", "1920x1080")
    VIDEO_FPS: int = int(os.getenv("VIDEO_FPS", "30"))
    
    # Output Settings
    OUTPUT_FORMAT: str = os.getenv("OUTPUT_FORMAT", "mp4")
    
    def __init__(self):
        """Initialize settings and create necessary directories."""
        self._create_directories()
    
    def _create_directories(self):
        """Create asset directories if they don't exist."""
        for directory in [self.AUDIO_DIR, self.VIDEO_DIR, self.OUTPUT_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def validate(self) -> bool:
        """Validate required settings."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True


# Global settings instance
settings = Settings()
