#!/usr/bin/env python3
"""
Setup script to download prerequisites for AI Media Orchestrator.
Downloads Piper TTS models and verifies FFmpeg availability.
"""

import os
import sys
import shutil
import requests
from pathlib import Path
import imageio_ffmpeg

# Configuration
PIPER_MODEL_NAME = "en_US-lessac-medium"
PIPER_MODEL_URL = f"https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/{PIPER_MODEL_NAME}.onnx"
PIPER_CONFIG_URL = f"https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/{PIPER_MODEL_NAME}.onnx.json"

BASE_DIR = Path(__file__).parent / "src" / "ai_media_orchestrator" / "assets"
MODELS_DIR = BASE_DIR / "models" / "piper"

def setup_directories():
    """Create necessary directories."""
    print(f"Creating directories in {BASE_DIR}...")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url: str, dest_path: Path):
    """Download a file from URL to destination path."""
    if dest_path.exists():
        print(f"File already exists: {dest_path}")
        return

    print(f"Downloading {url} to {dest_path}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        if dest_path.exists():
            dest_path.unlink()
        sys.exit(1)

def setup_piper():
    """Download Piper TTS model files."""
    print("\n--- Setting up Piper TTS ---")
    model_path = MODELS_DIR / f"{PIPER_MODEL_NAME}.onnx"
    config_path = MODELS_DIR / f"{PIPER_MODEL_NAME}.onnx.json"

    download_file(PIPER_MODEL_URL, model_path)
    download_file(PIPER_CONFIG_URL, config_path)
    
    print(f"Piper models ready at {MODELS_DIR}")

def verify_ffmpeg():
    """Verify FFmpeg availability via imageio-ffmpeg."""
    print("\n--- Verifying FFmpeg ---")
    try:
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"FFmpeg found at: {ffmpeg_path}")
        
        # Test execution
        import subprocess
        result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("FFmpeg verification successful.")
            print(result.stdout.split('\n')[0])
        else:
            print("FFmpeg verification failed.")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error verifying FFmpeg: {e}")
        print("Please ensure imageio-ffmpeg is installed.")
        sys.exit(1)

def main():
    print("Starting setup of prerequisites...")
    setup_directories()
    setup_piper()
    verify_ffmpeg()
    print("\nAll prerequisites setup successfully!")

if __name__ == "__main__":
    main()
