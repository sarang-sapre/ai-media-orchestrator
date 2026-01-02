import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path so we can import modules
sys.path.append(str(Path("src").absolute()))

from ai_media_orchestrator.modules.stock_video import StockVideoFetcher

# Load env
load_dotenv()

def verify():
    print("🧪 Verifying Pixabay Integration...")
    
    # Check key
    api_key = os.getenv("PIXABAY_API_KEY")
    if not api_key:
        print("❌ PIXABAY_API_KEY not found in environment variables.")
        print("Please add 'PIXABAY_API_KEY=your_key' to your .env file.")
        sys.exit(1)

    fetcher = StockVideoFetcher()
    
    # Test Search
    print("🔍 Testing search for 'nature'...")
    try:
        videos = fetcher.search_videos("nature", count=1)
    except Exception as e:
        print(f"❌ Search raised an exception: {e}")
        sys.exit(1)
    
    if not videos:
        print("❌ Search returned no results. Check if your API key is valid.")
        sys.exit(1)
        
    print(f"✅ Search successful. Found {len(videos)} video(s).")
    video = videos[0]
    print(f"   Video ID: {video['id']}")
    print(f"   URL: {video['url']}")
    
    # Test Download
    video_url = video['url']
    print(f"⬇️  Testing download...")
    
    output_path = Path("temp_test_video.mp4")
    # Clean up previous run
    if output_path.exists():
        output_path.unlink()
        
    try:
        downloaded_path = fetcher.download_video(video_url, output_path)
        
        if downloaded_path.exists() and downloaded_path.stat().st_size > 0:
            print(f"✅ Download successful: {downloaded_path} ({downloaded_path.stat().st_size} bytes)")
        else:
            print("❌ Download file missing or empty.")
            sys.exit(1)
            
        # Cleanup
        if downloaded_path.exists():
            downloaded_path.unlink()
            print("🧹 Cleanup successful.")
            
    except Exception as e:
        print(f"❌ Download failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify()
