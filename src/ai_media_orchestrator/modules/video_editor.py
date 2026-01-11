"""
Video editing module using FFmpeg directly.
"""

import subprocess
import imageio_ffmpeg
from pathlib import Path
from typing import List, Optional

from ai_media_orchestrator.config import settings


class VideoEditor:
    """
    Handles video editing operations using FFmpeg directly.
    """
    
    def __init__(self):
        """Initialize the video editor."""
        self.output_dir = settings.OUTPUT_DIR
        self.fps = settings.VIDEO_FPS
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    def _run_ffmpeg(self, cmd: List[str]):
        """Helper to run ffmpeg command."""
        try:
            # -y to overwrite output
            full_cmd = [self.ffmpeg_exe, "-y"] + cmd
            result = subprocess.run(
                full_cmd,
                check=True,
                capture_output=True,
                text=True
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg Error: {e.stderr}")
            raise RuntimeError(f"FFmpeg command failed: {e.stderr}") from e
            
    def get_media_duration(self, file_path: Path) -> float:
        """Get duration of media file in seconds using ffprobe."""
        cmd = [
            self.ffmpeg_exe.replace("ffmpeg", "ffprobe"),
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(file_path)
        ]
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return float(result.stdout.strip())
        except Exception as e:
            print(f"Error getting duration for {file_path}: {e}")
            return 0.0

    def combine_video_and_audio(
        self,
        video_path: Path,
        audio_path: Path,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Combine video with audio track using FFmpeg.
        Replaces audio in video with the provided audio file.
        Loops video if audio is longer, or cuts audio if video is longer? 
        Standard behavior: usually replace audio stream.
        """
        if output_path is None:
            output_path = self.output_dir / "final_video.mp4"
        
        # Command: ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
        # We also want to ensure the audio replaces existing audio (if any).
        # And we might want to trim/loop. For simple replace:
        
        # Loop video indefinitely and cut at audio length
        cmd = [
            "-stream_loop", "-1",  # Loop input 0 (video) indefinitely
            "-i", str(video_path),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",  # Finish when shortest input (audio) ends
            "-fflags", "+shortest", 
            str(output_path)
        ]
        
        self._run_ffmpeg(cmd)
        return output_path
    
    def concatenate_videos(
        self,
        video_paths: List[Path],
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Concatenate multiple videos into one using FFmpeg concat demuxer.
        """
        if output_path is None:
            output_path = self.output_dir / "concatenated_video.mp4"
            
        # Create a temporary file list for ffmpeg concat
        list_file_path = self.output_dir / "files.txt"
        with open(list_file_path, "w") as f:
            for path in video_paths:
                # Escape path if necessary, but absolute path usually works.
                # FFmpeg concat file requires 'file ' prefix and safe paths.
                safe_path = str(path.absolute()).replace("\\", "/")
                f.write(f"file '{safe_path}'\n")
        
        cmd = [
            "-f", "concat",
            "-safe", "0",
            "-i", str(list_file_path),
            "-c", "copy",
            str(output_path)
        ]
        
        self._run_ffmpeg(cmd)
        
        # Cleanup list file
        list_file_path.unlink(missing_ok=True)
        
        return output_path
    
    def trim_video(
        self,
        video_path: Path,
        start_time: float,
        end_time: float,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Trim video to specified time range using FFmpeg.
        """
        if output_path is None:
            output_path = self.output_dir / "trimmed_video.mp4"
        
        duration = end_time - start_time
        
        cmd = [
            "-ss", str(start_time),
            "-i", str(video_path),
            "-t", str(duration),
            "-c", "copy",  # Fast seek/copy. might not be frame accurate. re-encoding is safer for precision but slower.
            # For robustness, let's re-encode lightly or use copy if accepted. 
            # Re-encoding ensures precise cuts.
            # "-c:v", "libx264", "-c:a", "aac",
            str(output_path)
        ]
        
        # Note: placing -ss before -i is faster (input seeking).
        
        self._run_ffmpeg(cmd)
        return output_path
    
    def normalize_video(
        self,
        video_path: Path,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Normalize video to standard format (H.264, AAC, 30fps, 1280x720) to ensure smooth concatenation.
        """
        if output_path is None:
            output_path = self.output_dir / f"norm_{video_path.name}"
            
        # Parse resolution from settings
        try:
            width, height = settings.VIDEO_RESOLUTION.split("x")
        except ValueError:
            width, height = "1920", "1080"
            
        cmd = [
            "-i", str(video_path),
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,fps={self.fps}",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            "-ar", "44100",
            "-ac", "2",
            str(output_path)
        ]
        
        self._run_ffmpeg(cmd)
        return output_path

    def create_video_from_clips(
        self,
        video_clips: List[Path],
        audio_path: Path,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Create final video from multiple clips and audio.
        """
        # Normalize all clips first
        normalized_clips = []
        print("  ...normalizing video clips for concatenation...")
        for i, clip in enumerate(video_clips):
            try:
                norm_path = self.output_dir / f"norm_clip_{i}.mp4"
                self.normalize_video(clip, output_path=norm_path)
                normalized_clips.append(norm_path)
            except Exception as e:
                print(f"Warning: Failed to normalize clip {clip}: {e}")
        
        if not normalized_clips:
            raise ValueError("No valid video clips to process.")

        # First concatenate
        concat_video = self.output_dir / "temp_concat.mp4"
        self.concatenate_videos(normalized_clips, output_path=concat_video)
        
        # Cleanup normalized clips
        for clip in normalized_clips:
            try:
                clip.unlink(missing_ok=True)
            except Exception:
                pass
        
        # Then add audio (and trim/loop if needed)
        # Note: If the concatenated video is shorter/longer than audio?
        # Ideally we loop video or trim. For now, we just combine.
        
        final_video = self.combine_video_and_audio(
            concat_video,
            audio_path,
            output_path
        )
        
        # Cleanup temp
        concat_video.unlink(missing_ok=True)
        
        return final_video

    def generate_dummy_video(
        self,
        duration: float,
        output_path: Optional[Path] = None,
        color: str = "blue"
    ) -> Path:
        """
        Generate a solid color video using FFmpeg.
        """
        if output_path is None:
            output_path = self.output_dir / "dummy_video.mp4"
            
        # Parse resolution
        try:
            width, height = settings.VIDEO_RESOLUTION.split("x")
        except ValueError:
            width, height = "1920", "1080"
            
        cmd = [
            "-f", "lavfi",
            "-i", f"color=c={color}:s={width}x{height}:d={duration}",
            "-c:v", "libx264",
            "-t", str(duration),
            str(output_path)
        ]
        
        self._run_ffmpeg(cmd)
        return output_path
