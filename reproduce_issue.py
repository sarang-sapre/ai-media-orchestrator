import sys
from pathlib import Path
import traceback

# Add src to path
sys.path.append(str(Path.cwd() / "src"))

from ai_media_orchestrator.modules.voice_generator import VoiceGenerator
from ai_media_orchestrator.modules.video_editor import VideoEditor
from ai_media_orchestrator.config import settings

def test_audio():
    print("\n--- Testing Audio Generation ---")
    try:
        vg = VoiceGenerator()
        output_path = settings.AUDIO_DIR / "test_audio.wav"
        text = "This is a test of the audio generation system."
        generated_path = vg.generate_voice(text, output_path=output_path)
        
        if generated_path.exists():
            size = generated_path.stat().st_size
            print(f"✅ Audio generated at: {generated_path}")
            print(f"Size: {size} bytes")
            if size < 100:
                print("❌ Audio file seems too small (empty?)")
            else:
                print("✅ Audio file size looks reasonable.")
        else:
            print("❌ Audio file was not created.")
            
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        traceback.print_exc()

def test_video_concat():
    print("\n--- Testing Video Concatenation ---")
    try:
        ve = VideoEditor()
        
        # Create two dummy clips with potentially different properties (though generate_dummy_video uses defaults)
        # To simulate difference, we might need real clips, but let's start with basic concatenation validty.
        clip1 = ve.generate_dummy_video(duration=2, output_path=settings.VIDEO_DIR / "clip1.mp4", color="red")
        clip2 = ve.generate_dummy_video(duration=2, output_path=settings.VIDEO_DIR / "clip2.mp4", color="blue")
        
        concat_out = settings.OUTPUT_DIR / "test_concat.mp4"
        ve.concatenate_videos([clip1, clip2], output_path=concat_out)
        
        if concat_out.exists():
            size = concat_out.stat().st_size
            print(f"✅ Concatenated video generated at: {concat_out}")
            print(f"Size: {size} bytes")
            if size < 1000:
                 print("❌ Video file seems too small.")
        else:
            print("❌ Concatenated video not created.")

    except Exception as e:
        print(f"❌ Video test failed: {e}")
        traceback.print_exc()

def main():
    # Ensure directories exist
    settings.AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    settings.VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    test_audio()
    test_video_concat()

if __name__ == "__main__":
    main()
