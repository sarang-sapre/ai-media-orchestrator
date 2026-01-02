"""
Basic tests for AI Media Orchestrator.
"""

import pytest
from ai_media_orchestrator import __version__
from ai_media_orchestrator.config import settings


def test_version():
    """Test that version is defined."""
    assert __version__ == "0.1.0"


def test_settings_initialization():
    """Test that settings are initialized correctly."""
    assert settings.VERSION == "0.1.0"
    assert settings.OPENAI_MODEL == "gpt-4"
    assert settings.VIDEO_FPS == 30


def test_asset_directories_exist():
    """Test that asset directories are created."""
    assert settings.AUDIO_DIR.exists()
    assert settings.VIDEO_DIR.exists()
    assert settings.OUTPUT_DIR.exists()


# TODO: Add more comprehensive tests for each module
# - test_script_generator.py
# - test_voice_generator.py
# - test_stock_video.py
# - test_video_editor.py
# - test_subtitles.py
