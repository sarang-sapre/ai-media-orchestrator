"""
Configuration management for AI Media Orchestrator.
Loads settings from environment variables.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables before settings are initialized
load_dotenv()


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
    
    # AI Provider Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "auto")  # 'gemini', 'openai', or 'auto'
    
    # Google Gemini Configuration (Free tier available!)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
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
    
    def get_active_provider(self) -> str:
        """Determine which AI provider to use based on configuration."""
        if self.AI_PROVIDER == "auto":
            # Auto-select: prefer Gemini (free) if available, otherwise OpenAI
            if self.GEMINI_API_KEY:
                return "gemini"
            elif self.OPENAI_API_KEY:
                return "openai"
            else:
                raise ValueError("No AI API key configured. Please set GEMINI_API_KEY or OPENAI_API_KEY")
        elif self.AI_PROVIDER == "gemini":
            if not self.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is required when AI_PROVIDER is set to 'gemini'")
            return "gemini"
        elif self.AI_PROVIDER == "openai":
            if not self.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required when AI_PROVIDER is set to 'openai'")
            return "openai"
        else:
            raise ValueError(f"Invalid AI_PROVIDER: {self.AI_PROVIDER}. Must be 'gemini', 'openai', or 'auto'")
    
    def validate(self) -> bool:
        """Validate required settings."""
        # Check that at least one AI provider is configured
        if not self.GEMINI_API_KEY and not self.OPENAI_API_KEY:
            raise ValueError(
                "At least one AI API key is required. "
                "Please set GEMINI_API_KEY (free) or OPENAI_API_KEY in your .env file"
            )
        # Validate the active provider
        self.get_active_provider()
        return True


# Global settings instance
settings = Settings()
