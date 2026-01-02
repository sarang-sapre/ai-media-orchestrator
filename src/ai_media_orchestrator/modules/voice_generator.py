"""
Voice generation module using OpenAI TTS.
"""

from pathlib import Path
from typing import Optional
from openai import OpenAI

from ai_media_orchestrator.config import settings


class VoiceGenerator:
    """
    Generates voice audio from text using OpenAI's Text-to-Speech API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the voice generator.
        
        Args:
            api_key: OpenAI API key. If None, uses settings.OPENAI_API_KEY
        """
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key)
        self.model = settings.VOICE_MODEL
        self.voice = settings.VOICE_NAME
    
    def generate_voice(
        self,
        text: str,
        output_path: Optional[Path] = None,
        voice: Optional[str] = None,
        **kwargs
    ) -> Path:
        """
        Generate voice audio from text.
        
        Args:
            text: The text to convert to speech
            output_path: Path to save the audio file. If None, auto-generates in AUDIO_DIR
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            **kwargs: Additional parameters to pass to the API
        
        Returns:
            Path to the generated audio file
        """
        if output_path is None:
            output_path = settings.AUDIO_DIR / "generated_voice.mp3"
        
        voice = voice or self.voice
        
        response = self.client.audio.speech.create(
            model=self.model,
            voice=voice,
            input=text,
            **kwargs
        )
        
        # Save the audio file
        response.stream_to_file(output_path)
        
        return output_path
    
    def get_available_voices(self) -> list[str]:
        """
        Get list of available voices.
        
        Returns:
            List of voice names
        """
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
