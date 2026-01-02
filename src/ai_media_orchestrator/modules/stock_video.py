"""
Stock video fetching module.
"""

from pathlib import Path
from typing import List, Optional
import requests

from ai_media_orchestrator.config import settings


class StockVideoFetcher:
    """
    Fetches stock videos from various sources.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the stock video fetcher.
        
        Args:
            api_key: API key for stock video service (e.g., Pexels, Pixabay)
        """
        self.api_key = settings.STOCK_VIDEO_API_KEY
        self.video_dir = settings.VIDEO_DIR
    
    def search_videos(
        self,
        query: str,
        count: int = 5,
        orientation: str = "landscape"
    ) -> List[dict]:
        """
        Search for stock videos based on query.
        
        Args:
            query: Search query for videos
            count: Number of videos to fetch
            orientation: Video orientation (landscape, portrait, square)
        
        Returns:
            List of video metadata dictionaries
        """
        if not self.api_key:
            print("⚠️ No Stock Video API key found. Please set PIXABAY_API_KEY in .env.")
            return []

        print(f"🔍 Searching for videos: {query}")
        
        base_url = "https://pixabay.com/api/videos/"
        params = {
            "key": self.api_key,
            "q": query,
            "per_page": count,
            "video_type": "all"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            videos = []
            for hit in data.get("hits", []):
                # Pixabay provides different sizes. 
                # We'll try to get 'medium' (approx 720p/1080p) or fallback to 'large' then 'small'.
                video_variants = hit.get("videos", {})
                variant = video_variants.get("medium") or video_variants.get("large") or video_variants.get("small")
                
                if variant:
                    videos.append({
                        "id": hit["id"],
                        "url": variant["url"],
                        "duration": hit["duration"],
                        "width": variant["width"],
                        "height": variant["height"],
                        "thumbnail": hit.get("userImageURL")  # Fallback to user image if video thumbnail not parsed
                    })
            
            return videos
            
        except Exception as e:
            print(f"❌ Error searching Pixabay: {e}")
            return []
    
    def download_video(
        self,
        url: str,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Download a video from URL.
        
        Args:
            url: URL of the video to download
            output_path: Path to save the video. If None, auto-generates
        
        Returns:
            Path to the downloaded video file
        """
        if output_path is None:
            filename = url.split("/")[-1]
            # Ensure filename has an extension if missing
            if "." not in filename:
                filename += ".mp4"
            output_path = self.video_dir / filename
            
        if output_path.exists():
            print(f"⏭️  Video already exists at: {output_path}")
            return output_path
        
        print(f"📥 Downloading video from: {url}")
        print(f"   Saving to: {output_path}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Download complete: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error downloading video: {e}")
            if output_path.exists():
                output_path.unlink()  # Remove partial file
            raise e
    
    def fetch_videos_for_script(
        self,
        script: str,
        keywords: Optional[List[str]] = None
    ) -> List[Path]:
        """
        Fetch relevant videos based on script content.
        
        Args:
            script: The video script
            keywords: Optional list of keywords to search for
        
        Returns:
            List of paths to downloaded videos
        """
        # TODO: Implement keyword extraction from script if not provided
        # TODO: Search and download videos for each keyword
        
        if keywords is None:
            keywords = ["nature", "technology"]  # Placeholder
        
        video_paths = []
        for keyword in keywords:
            videos = self.search_videos(keyword, count=5)
            for video in videos:
                path = self.download_video(video["url"])
                video_paths.append(path)
        
        return video_paths
