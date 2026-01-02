"""
Script generation module using OpenAI GPT models.
"""

from typing import Optional, Dict, Any
from openai import OpenAI

from ai_media_orchestrator.config import settings


class ScriptGenerator:
    """
    Generates video scripts using OpenAI's GPT models.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the script generator.
        
        Args:
            api_key: OpenAI API key. If None, uses settings.OPENAI_API_KEY
        """
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key)
        self.model = settings.OPENAI_MODEL
    
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
            **kwargs: Additional parameters to pass to the API
        
        Returns:
            Generated script text
        """
        prompt = self._build_prompt(topic, duration, style)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional video script writer."},
                {"role": "user", "content": prompt}
            ],
            **kwargs
        )
        
        return response.choices[0].message.content
    
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
