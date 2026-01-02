"""
Script generation module using AI (supports OpenAI and Google Gemini).
"""

from typing import Optional, Dict, Any

from ai_media_orchestrator.config import settings
from ai_media_orchestrator.modules.ai_client import AIClient


class ScriptGenerator:
    """
    Generates video scripts using AI models (OpenAI GPT or Google Gemini).
    """
    
    def __init__(self, provider: Optional[str] = None):
        """
        Initialize the script generator.
        
        Args:
            provider: AI provider to use ('gemini', 'openai', or None for auto-detection)
        """
        self.ai_client = AIClient(provider=provider)
    
    def generate_script(
        self,
        topic: str,
        duration: int = 60,
        style: str = "informative",
        **kwargs
    ) -> str:
        """
        Generate a video script for the given topic.
        
        Args:
            topic: The topic for the video script
            duration: Target duration in seconds
            style: Style of the script (informative, entertaining, educational, etc.)
            **kwargs: Additional parameters to pass to the AI API
        
        Returns:
            Generated script text
        """
        prompt = self._build_prompt(topic, duration, style)
        
        return self.ai_client.generate_text(
            prompt=prompt,
            system_message="You are a professional video script writer.",
            **kwargs
        )
    
    def _build_prompt(self, topic: str, duration: int, style: str) -> str:
        """Build the prompt for script generation."""
        return f"""
        Create a {style} video script about: {topic}
        
        Requirements:
        - Target duration: {duration} seconds
        - Style: {style}
        - Include engaging hook at the beginning
        - Clear structure with introduction, main content, and conclusion
        - Natural, conversational tone
        - Suitable for voiceover narration
        
        Please provide only the script text, without any additional formatting or labels.
        """

