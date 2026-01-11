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
    MODELS_DIR = ASSETS_DIR / "models"
    SCRIPTS_DIR = ASSETS_DIR / "scripts"

    
    # AI Provider Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "auto")  # 'gemini', 'openai', or 'auto'
    
    # Google Gemini Configuration (Free tier available!)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")

    # Ollama Configuration (Local LLM)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    
    # Voice Generation
    VOICE_MODEL: str = os.getenv("VOICE_MODEL", "tts-1")
    VOICE_MODEL: str = os.getenv("VOICE_MODEL", "tts-1")
    VOICE_NAME: str = os.getenv("VOICE_NAME", "alloy")
    
    # Piper TTS
    PIPER_MODEL_NAME: str = os.getenv("PIPER_MODEL_NAME", "en_US-lessac-medium")

    
    # Video Settings
    VIDEO_RESOLUTION: str = os.getenv("VIDEO_RESOLUTION", "1920x1080")
    VIDEO_FPS: int = int(os.getenv("VIDEO_FPS", "30"))
    
    # Stock Video Settings
    STOCK_VIDEO_API_KEY: Optional[str] = os.getenv("PIXABAY_API_KEY")
    
    # Output Settings
    OUTPUT_FORMAT: str = os.getenv("OUTPUT_FORMAT", "mp4")
    
    def __init__(self):
        """Initialize settings and create necessary directories."""
        self._create_directories()
    
    def _create_directories(self):
        """Create asset directories if they don't exist."""
        for directory in [self.AUDIO_DIR, self.VIDEO_DIR, self.OUTPUT_DIR, self.MODELS_DIR, self.SCRIPTS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_active_provider(self) -> str:
        """Determine which AI provider to use based on configuration."""
        if self.AI_PROVIDER == "auto":
            # Auto-select: prefer Gemini (free) if available, otherwise OpenAI, then Ollama
            if self.GEMINI_API_KEY:
                return "gemini"
            elif self.OPENAI_API_KEY:
                return "openai"
            else:
                # Fallback to Ollama if no keys are present (assuming local setup)
                return "ollama"
        elif self.AI_PROVIDER == "gemini":
            if not self.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is required when AI_PROVIDER is set to 'gemini'")
            return "gemini"
        elif self.AI_PROVIDER == "openai":
            if not self.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required when AI_PROVIDER is set to 'openai'")
            return "openai"
        elif self.AI_PROVIDER == "ollama":
            return "ollama"
        else:
            raise ValueError(f"Invalid AI_PROVIDER: {self.AI_PROVIDER}. Must be 'gemini', 'openai', 'ollama', or 'auto'")
    
    def validate(self) -> bool:
        """Validate required settings."""
        # Check that at least one AI provider is configured
        if not self.GEMINI_API_KEY and not self.OPENAI_API_KEY and self.AI_PROVIDER != "ollama":
            # If auto mode, we default to ollama if keys are missing, so this might not be reached in auto mode 
            # unless we want to strictly enforce keys for cloud providers.
            # But let's assume if no keys, we might be trying ollama.
            pass
        # Validate the active provider
        self.get_active_provider()
        return True


# Global settings instance
settings = Settings()
