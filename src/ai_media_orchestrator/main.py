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
        script_text, keywords = script_gen.generate_script(topic, duration=30, style="engaging")
        print("✅ Script generated!")
        print(f"Preview: {script_text[:100]}...\n")
        print(f"Visual Keywords: {keywords}")
        
        # 2. Generate Voiceover
        print("🗣️  Generating voiceover...")
        audio_path = settings.AUDIO_DIR / "voiceover.wav"
        voice_gen.generate_voice(script_text, output_path=audio_path)
        print(f"✅ Voiceover saved to: {audio_path}")
        
        # Get audio duration
        audio_duration = video_editor.get_media_duration(audio_path)
        print(f"⏱️  Audio duration: {audio_duration:.2f}s")
        
        # 3. Fetch Stock Videos (or fallback)
        print("\n🎥 Fetching visual assets...")
        video_clips = []
        
        # Calculate how many clips we need (approx 5-10s per clip)
        target_clip_count = max(5, int(audio_duration / 5) + 2) # +2 for safety
        
        if keywords:
            # Use generated keywords
            print(f"   Searching for: {', '.join(keywords)}")
            for keyword in keywords:
                if len(video_clips) >= target_clip_count:
                    break
                new_clips = stock_fetcher.fetch_videos_for_script(script_text, keywords=[keyword])
                video_clips.extend(new_clips)
        
        # If we still don't have enough, fill with generic
        if len(video_clips) < target_clip_count:
            print("   Fetching additional generic clips...")
            generic_keywords = [topic.split()[0], "abstract", "technology", "nature", "background"]
            for keyword in generic_keywords:
                if len(video_clips) >= target_clip_count:
                    break
                new_clips = stock_fetcher.fetch_videos_for_script(script_text, keywords=[keyword])
                video_clips.extend(new_clips)
        
        # Dedup clips (by path)
        video_clips = list(dict.fromkeys(video_clips))
        
        final_video_path = settings.OUTPUT_DIR / "final_output.mp4"
        
        if video_clips:
            print(f"✅ Fetched {len(video_clips)} clips.")
            print("✂️  Editing video...")
            video_editor.create_video_from_clips(video_clips, audio_path, output_path=final_video_path)
        else:
            print("⚠️  No stock videos found (check API key). Generating dummy video instead.")
            video_editor.generate_dummy_video(duration=audio_duration, output_path=settings.VIDEO_DIR / "dummy_base.mp4")
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
