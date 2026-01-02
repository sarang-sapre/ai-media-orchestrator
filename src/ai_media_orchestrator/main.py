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
    print(f"Active Provider: {settings.get_active_provider().upper()}")
    print("-" * 50)
    
    try:
        # Initialize components
        script_gen = ScriptGenerator() # Uses AI_PROVIDER (Ollama)
        voice_gen = VoiceGenerator()   # Uses Piper TTS
        video_editor = VideoEditor()   # Uses FFmpeg
        stock_fetcher = StockVideoFetcher() # Uses Pixabay
        
        # 1. Generate Script
        topic = input("Enter a topic for the video: ") or "Artificial Intelligence"
        print(f"\n📝 Generating script for topic: '{topic}'...")
        script = script_gen.generate_script(topic, duration=30, style="engaging")
        print("✅ Script generated!")
        print(f"Preview: {script[:100]}...\n")
        
        # 2. Generate Voiceover
        print("🗣️  Generating voiceover...")
        audio_path = settings.AUDIO_DIR / "voiceover.wav"
        voice_gen.generate_voice(script, output_path=audio_path)
        print(f"✅ Voiceover saved to: {audio_path}")
        
        # Get audio duration (approximate or use ffprobe? For now, assume script length or just use fallback)
        # We need duration to fetch enough stock videos. 
        # A simple estimation: 150 words ~ 1 minute.
        
        # 3. Fetch Stock Videos (or fallback)
        print("\n🎥 Fetching visual assets...")
        # Extract simple keyword from topic
        keyword = topic.split()[0] 
        video_clips = stock_fetcher.fetch_videos_for_script(script, keywords=[keyword, "abstract"])
        
        final_video_path = settings.OUTPUT_DIR / "final_output.mp4"
        
        if video_clips:
            print(f"✅ Fetched {len(video_clips)} clips.")
            print("✂️  Editing video...")
            video_editor.create_video_from_clips(video_clips, audio_path, output_path=final_video_path)
        else:
            print("⚠️  No stock videos found (check API key). Generating dummy video instead.")
            # Estimate duration from audio file size? Or just hardcode 30s.
            # Ideally we check audio length.
            # For simplicity, stick to requested 30s script duration.
            video_editor.generate_dummy_video(duration=30, output_path=settings.VIDEO_DIR / "dummy_base.mp4")
            video_editor.combine_video_and_audio(
                settings.VIDEO_DIR / "dummy_base.mp4",
                audio_path,
                output_path=final_video_path
            )

        print(f"\n✨ DONE! Final video available at: {final_video_path}")
        
    except Exception as e:
        print(f"\n❌ Error in orchestration pipeline: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
