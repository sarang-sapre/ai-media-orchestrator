"""
Main entry point for AI Media Orchestrator.
"""

import os
from dotenv import load_dotenv

from ai_media_orchestrator.config import settings
from ai_media_orchestrator.modules.script_generator import ScriptGenerator
from ai_media_orchestrator.modules.voice_generator import VoiceGenerator
from ai_media_orchestrator.modules.stock_video import StockVideoFetcher
from ai_media_orchestrator.modules.video_editor import VideoEditor
from ai_media_orchestrator.modules.subtitles import SubtitleGenerator


def main():
    """
    Main orchestration function.
    """
    # Load environment variables
    load_dotenv()
    
    print("🎬 AI Media Orchestrator")
    print(f"Version: {settings.VERSION}")
    print("-" * 50)
    
    # TODO: Implement orchestration workflow
    # 1. Generate script
    # 2. Generate voice
    # 3. Fetch stock videos
    # 4. Edit video
    # 5. Generate subtitles
    
    print("✅ Orchestration pipeline ready!")


if __name__ == "__main__":
    main()
