import sys
import subprocess
from pathlib import Path
from typing import Optional, List

from ai_media_orchestrator.config import settings


class VoiceGenerator:
    """
    Generates voice audio from text using Piper TTS (local) via CLI subprocess.
    """

    def __init__(self):
        """
        Initialize the voice generator.
        Loads the Piper model configuration paths.
        """
        self.model_name = settings.PIPER_MODEL_NAME
        self.model_path = settings.MODELS_DIR / "piper" / f"{self.model_name}.onnx"
        self.config_path = settings.MODELS_DIR / "piper" / f"{self.model_name}.onnx.json"

        if not self.model_path.exists() or not self.config_path.exists():
            raise FileNotFoundError(
                f"Piper model not found at {self.model_path}. "
                "Please run setup_prerequisites.py to download it."
            )

    def generate_voice(
        self,
        text: str,
        output_path: Optional[Path] = None,
        voice: Optional[str] = None,  # kept for API compatibility
        **kwargs,
    ) -> Path:
        """
        Generate voice audio from text using Piper CLI.

        Args:
            text: The text to convert to speech
            output_path: Path to save the audio file. If None, auto-generates in AUDIO_DIR
            voice: Ignored (using configured model)

        Returns:
            Path to the generated audio file
        """
        if not text:
            raise ValueError("Cannot generate voice for empty text.")

        if output_path is None:
            output_path = settings.AUDIO_DIR / "generated_voice.wav"

        wav_path = output_path.with_suffix(".wav")
        
        # Ensure directory exists
        wav_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"DEBUG: Generating voice using Piper CLI for model: {self.model_name}")
        
        try:
            # Construct command: echo "text" | python -m piper -m model -f output
            # We use subprocess.communicate to send text to stdin
            cmd = [
                sys.executable,
                "-m",
                "piper",
                "--model",
                str(self.model_path),
                "--output_file",
                str(wav_path)
            ]
            
            print(f"DEBUG: Running command: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text)
            
            if process.returncode != 0:
                print(f"ERROR: Piper CLI failed with code {process.returncode}")
                print(f"Stderr: {stderr}")
                raise RuntimeError(f"Piper CLI failed: {stderr}")
            
            # Check if file was created and has content
            if wav_path.exists():
                size = wav_path.stat().st_size
                print(f"DEBUG: Generated WAV size: {size} bytes")
                if size < 1000: # Less than 1KB is suspicious
                    print("WARNING: Generated audio is suspiciously small!")
            else:
                 raise RuntimeError("WAV file was not created by Piper CLI.")

        except Exception as e:
            print(f"ERROR: Voice generation failed: {e}")
            raise

        # Convert to requested format if needed
        if output_path.suffix.lower() != ".wav":
            self._convert_to_format(wav_path, output_path)

        return output_path

    def _convert_to_format(self, input_path: Path, output_path: Path):
        """Convert audio using FFmpeg."""
        import imageio_ffmpeg

        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        cmd = [
            ffmpeg_exe,
            "-y",
            "-i",
            str(input_path),
            "-ac",
            "1",
            "-ar",
            "22050",
            str(output_path),
        ]

        subprocess.run(cmd, check=True, capture_output=True)

    def get_available_voices(self) -> List[str]:
        """Return available voice models."""
        return [self.model_name]
