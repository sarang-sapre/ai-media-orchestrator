"""
Subtitle generation module using OpenAI Whisper.
"""

from pathlib import Path
from typing import Optional, List, Dict
import whisper

from ai_media_orchestrator.config import settings


class SubtitleGenerator:
    """
    Generates subtitles from audio using OpenAI Whisper.
    """
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize the subtitle generator.
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.model = None
    
    def load_model(self):
        """Load the Whisper model."""
        if self.model is None:
            print(f"📥 Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)
    
    def transcribe_audio(
        self,
        audio_path: Path,
        language: Optional[str] = None
    ) -> Dict:
        """
        Transcribe audio file to text with timestamps.
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en', 'es'). If None, auto-detects
        
        Returns:
            Dictionary with transcription results including segments
        """
        self.load_model()
        
        print(f"🎤 Transcribing audio: {audio_path}")
        
        result = self.model.transcribe(
            str(audio_path),
            language=language,
            task="transcribe"
        )
        
        return result
    
    def generate_srt(
        self,
        audio_path: Path,
        output_path: Optional[Path] = None,
        language: Optional[str] = None
    ) -> Path:
        """
        Generate SRT subtitle file from audio.
        
        Args:
            audio_path: Path to audio file
            output_path: Path for output SRT file. If None, auto-generates
            language: Language code. If None, auto-detects
        
        Returns:
            Path to the generated SRT file
        """
        if output_path is None:
            output_path = settings.OUTPUT_DIR / "subtitles.srt"
        
        # Transcribe audio
        result = self.transcribe_audio(audio_path, language)
        
        # Generate SRT content
        srt_content = self._create_srt_content(result["segments"])
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        print(f"✅ Subtitles saved to: {output_path}")
        
        return output_path
    
    def _create_srt_content(self, segments: List[Dict]) -> str:
        """
        Create SRT formatted content from segments.
        
        Args:
            segments: List of transcription segments with timestamps
        
        Returns:
            SRT formatted string
        """
        srt_lines = []
        
        for i, segment in enumerate(segments, start=1):
            start_time = self._format_timestamp(segment["start"])
            end_time = self._format_timestamp(segment["end"])
            text = segment["text"].strip()
            
            srt_lines.append(f"{i}")
            srt_lines.append(f"{start_time} --> {end_time}")
            srt_lines.append(text)
            srt_lines.append("")  # Empty line between subtitles
        
        return "\n".join(srt_lines)
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Format seconds to SRT timestamp format (HH:MM:SS,mmm).
        
        Args:
            seconds: Time in seconds
        
        Returns:
            Formatted timestamp string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
