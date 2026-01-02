
import logging
from pathlib import Path
from ai_media_orchestrator.modules.voice_generator import VoiceGenerator

logging.basicConfig(level=logging.DEBUG)

def main():
    print("Testing Piper TTS isolation...")
    try:
        vg = VoiceGenerator()
        print(f"Model path: {vg.model_path}")
        print(f"Exists: {vg.model_path.exists()}")
        
        output = Path("test_piper_output.wav").resolve()
        vg.generate_voice("Testing 1 2 3", output_path=output)
        
        if output.exists():
            print(f"Success! Output at {output}")
        else:
            print("Failure! Output file not found.")
            
    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
