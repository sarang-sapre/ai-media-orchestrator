"""
Video editing module using MoviePy.
"""

from pathlib import Path
from typing import List, Optional
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip
)

from ai_media_orchestrator.config import settings


class VideoEditor:
    """
    Handles video editing operations using MoviePy.
    """
    
    def __init__(self):
        """Initialize the video editor."""
        self.output_dir = settings.OUTPUT_DIR
        self.fps = settings.VIDEO_FPS
    
    def combine_video_and_audio(
        self,
        video_path: Path,
        audio_path: Path,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Combine video with audio track.
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_path: Path for output file. If None, auto-generates
        
        Returns:
            Path to the output video file
        """
        if output_path is None:
            output_path = self.output_dir / "final_video.mp4"
        
        video = VideoFileClip(str(video_path))
        audio = AudioFileClip(str(audio_path))
        
        # Set audio to video
        final_video = video.set_audio(audio)
        
        # Write output
        final_video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Clean up
        video.close()
        audio.close()
        final_video.close()
        
        return output_path
    
    def concatenate_videos(
        self,
        video_paths: List[Path],
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Concatenate multiple videos into one.
        
        Args:
            video_paths: List of paths to video files
            output_path: Path for output file. If None, auto-generates
        
        Returns:
            Path to the concatenated video file
        """
        if output_path is None:
            output_path = self.output_dir / "concatenated_video.mp4"
        
        clips = [VideoFileClip(str(path)) for path in video_paths]
        final_clip = concatenate_videoclips(clips)
        
        final_clip.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Clean up
        for clip in clips:
            clip.close()
        final_clip.close()
        
        return output_path
    
    def trim_video(
        self,
        video_path: Path,
        start_time: float,
        end_time: float,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Trim video to specified time range.
        
        Args:
            video_path: Path to video file
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Path for output file. If None, auto-generates
        
        Returns:
            Path to the trimmed video file
        """
        if output_path is None:
            output_path = self.output_dir / "trimmed_video.mp4"
        
        video = VideoFileClip(str(video_path))
        trimmed = video.subclip(start_time, end_time)
        
        trimmed.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Clean up
        video.close()
        trimmed.close()
        
        return output_path
    
    def create_video_from_clips(
        self,
        video_clips: List[Path],
        audio_path: Path,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Create final video from multiple clips and audio.
        
        Args:
            video_clips: List of video clip paths
            audio_path: Path to audio file
            output_path: Path for output file. If None, auto-generates
        
        Returns:
            Path to the final video file
        """
        # First concatenate all video clips
        concatenated = self.concatenate_videos(video_clips)
        
        # Then add audio
        final_video = self.combine_video_and_audio(
            concatenated,
            audio_path,
            output_path
        )
        
        return final_video
