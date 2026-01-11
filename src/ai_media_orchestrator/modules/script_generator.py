"""
Script generation module using AI (supports OpenAI and Google Gemini).
"""

import re
from datetime import datetime
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
    ) -> tuple[str, list[str]]:
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
        
        response = self.ai_client.generate_text(
            prompt=prompt,
            system_message="You are a professional video script writer.",
            **kwargs
        )

        print(f"DEBUG_RAW_RESPONSE:\n{response}\nEND_DEBUG_RAW_RESPONSE")
        
        if "---SPLIT---" in response:
            # fast-forward: sometimes models repeat the instruction "separated by ---SPLIT---"
            # so we split from the right to safely get the keywords at the end.
            parts = response.rsplit("---SPLIT---", 1)
            raw_script_text = parts[0].strip()
            
            if len(parts) > 1:
                keywords_text = parts[1].strip()
                keywords = [k.strip() for k in keywords_text.split(",")]
            else:
                keywords = []
        else:
            raw_script_text = response.strip()
            keywords = []

        # Begin cleaning the script text
        script_text = raw_script_text
        
        # 0. Remove any stray ---SPLIT--- tokens that might have been left in the first part
        # (e.g. if the model said "Here is the output separated by ---SPLIT---")
        script_text = script_text.replace("---SPLIT---", "")

        # Post-processing cleanup
        # 1. If "Voiceover Script:" is present, take everything after it.
        #    This is the most reliable marker if the model follows the structure but leaks the header.
        if "voiceover script:" in script_text.lower():
            # Find the match case-insensitively
            match = re.search(r"(?i)voiceover script:", script_text)
            if match:
                script_text = script_text[match.end():].strip()

        # 2. Cleanup common conversational intros if they appear at the start
        # Regex to remove lines starting with "Here is..." or similar, up to a colon or newline
        # matching patterns like: "Here is the script:", "Here is the script for X:", "Sure, here it is:"
        script_text = re.sub(
            r"(?i)^(here is|here's|sure|certainly|preview|okay|ok).+?(:|\n)", 
            "", 
            script_text, 
            flags=re.DOTALL
        ).strip()
        
        # Save script to file
        self._save_script(topic, script_text)

        return script_text, keywords

    def _save_script(self, topic: str, content: str):
        """Save the generated script to a text file for reference."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sanitized_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
            filename = f"script_{timestamp}_{sanitized_topic[:30]}.txt"
            filepath = settings.SCRIPTS_DIR / filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Topic: {topic}\n")
                f.write(f"Date: {datetime.now()}\n")
                f.write("-" * 50 + "\n\n")
                f.write(content)
            
            print(f"DEBUG: Saved script to {filepath}")
        except Exception as e:
            print(f"WARNING: Failed to save script file: {e}")
    
    def _build_prompt(self, topic: str, duration: int, style: str) -> str:
        """
        Build a voiceover-optimized prompt for script generation.
        The output is designed to be directly converted into speech (TTS).
        """
        return f"""
You are a professional voiceover script writer.

Your task is to write a spoken narration script for a video.

Topic:
{topic}

Target duration:
{duration} seconds (approximately {duration * 2.2:.0f} to {duration * 2.5:.0f} words)

Style:
{style}

Voiceover Requirements:
- Write ONLY spoken words (no headings, no bullet points, no emojis)
- Use short, natural sentences suitable for text-to-speech
- Conversational and engaging tone
- No references to visuals like "on screen", "you can see", or "this video"
- No special characters, markdown, or formatting
- Avoid complex punctuation that can break TTS
- Smooth flow with natural pauses implied by sentence structure

Content Structure:
- Start with a strong hook in the first 2–3 sentences
- Clearly explain the topic in a simple, engaging way
- Maintain a logical flow from start to end
- End with a clear and satisfying conclusion or takeaway

IMPORTANT OUTPUT FORMAT (STRICT):
You MUST return the output in exactly TWO sections separated by:

---SPLIT---

Section 1: Voiceover Script
- Plain text narration only
- This text will be directly converted to speech
- DO NOT include "Voiceover Script:" or similar labels in the output text itself
- DO NOT include "Here is the script" or any intro text

Section 2: Visual Keywords
- A comma-separated list of 5 to 7 highly specific visual search keywords
- Keywords should describe imagery that matches the topic
- Do NOT use full sentences

Example Output:

The future of artificial intelligence is closer than you think. Every day, machines are learning faster and smarter...
---SPLIT---
artificial intelligence, neural network, futuristic city, robot assistant, data visualization
"""

