import os
import subprocess
from pathlib import Path
from ai_media_orchestrator.config import settings
from ai_media_orchestrator.modules.script_generator import ScriptGenerator
from ai_media_orchestrator.modules.voice_generator import VoiceGenerator
from ai_media_orchestrator.modules.video_editor import VideoEditor

def generate_dummy_video(path: Path, duration: int = 5):
    """Generate a dummy color video using FFmpeg."""
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "lavfi",
        "-i", f"color=c=blue:s=1280x720:d={duration}",
        "-c:v", "libx264",
        str(path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def main():
    print("--- Starting Stack Verification ---")
    
    # 1. Script Generation (Ollama)
    print("\n1. Testing Script Generation (Ollama)...")
    try:
        # Force provider to ollama for testing if not set
        if settings.AI_PROVIDER == "auto" and not settings.OLLAMA_BASE_URL:
             # Just assume auto works or manual override for test
             pass
        
        # We can pass provider explicitly
        script_gen = ScriptGenerator(provider="ollama")
        script = script_gen.generate_script("The history of AI", duration=10, style="concise")
        print(f"Script generated (preview): {script[:100]}...")
    except Exception as e:
        print(f"Script generation failed: {e}")
        # Proceeding to test other components even if this fails (e.g. if ollama server not running)
    
    # 2. Voice Generation (Piper)
    print("\n2. Testing Voice Generation (Piper)...")
    try:
        voice_gen = VoiceGenerator()
        text = "This is a test of the Piper text to speech system."
        audio_path = settings.AUDIO_DIR / "test_voice.wav"
        voice_gen.generate_voice(text, output_path=audio_path)
        print(f"Voice generated at: {audio_path}")
    except Exception as e:
        print(f"Voice generation failed: {e}")
        return

    # 3. Video Editing (FFmpeg)
    print("\n3. Testing Video Editing (FFmpeg)...")
    try:
        video_editor = VideoEditor()
        video_path = settings.VIDEO_DIR / "test_dummy.mp4"
        generate_dummy_video(video_path)
        
        # Combine
        output_path = settings.OUTPUT_DIR / "test_output.mp4"
        video_editor.combine_video_and_audio(video_path, audio_path, output_path)
        print(f"Final video generated at: {output_path}")
    except Exception as e:
        print(f"Video editing failed: {e}")

if __name__ == "__main__":
    main()
