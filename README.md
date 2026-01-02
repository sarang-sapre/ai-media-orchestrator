# AI Media Orchestrator

AI-powered orchestration pipeline for automating no-face videos and media content creation.

## 🚀 Features

- **AI-Powered Content Generation**: Leverage OpenAI's GPT models for script generation
- **Video Processing**: Automated video editing and composition using MoviePy
- **Audio Processing**: Speech-to-text transcription with OpenAI Whisper
- **Media Orchestration**: End-to-end pipeline for creating engaging media content

## 📋 Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

## 🛠️ Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/sarang-sapre/ai-media-orchestrator.git
cd ai-media-orchestrator

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# Install development dependencies
uv pip install -e ".[dev]"
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/sarang-sapre/ai-media-orchestrator.git
cd ai-media-orchestrator

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## 📁 Project Structure

```
ai-media-orchestrator/
├── src/
│   └── ai_media_orchestrator/
│       ├── __init__.py
│       ├── main.py              # Entry point
│       ├── config.py            # Settings & env vars
│       │
│       ├── modules/
│       │   ├── __init__.py
│       │   ├── script_generator.py
│       │   ├── voice_generator.py
│       │   ├── stock_video.py
│       │   ├── video_editor.py
│       │   └── subtitles.py
│       │
│       └── assets/
│           ├── audio/
│           ├── video/
│           └── output/
│
├── tests/
│   └── test_basic.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
└── uv.lock
```

## 🔧 Configuration

Create a `.env` file in the project root with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 💻 Usage

### Running the Main Pipeline

```bash
python -m ai_media_orchestrator.main
```

### Using Individual Modules

```python
from ai_media_orchestrator.modules import (
    ScriptGenerator,
    VoiceGenerator,
    StockVideoFetcher,
    VideoEditor,
    SubtitleGenerator
)

# Generate a script
script_gen = ScriptGenerator()
script = script_gen.generate_script(
    topic="The Future of AI",
    duration=60,
    style="informative"
)

# Generate voice from script
voice_gen = VoiceGenerator()
audio_path = voice_gen.generate_voice(script)

# Fetch stock videos
video_fetcher = StockVideoFetcher()
video_paths = video_fetcher.fetch_videos_for_script(script)

# Edit and combine
editor = VideoEditor()
final_video = editor.create_video_from_clips(video_paths, audio_path)

# Generate subtitles
subtitle_gen = SubtitleGenerator()
subtitle_path = subtitle_gen.generate_srt(audio_path)

print(f"✅ Video created: {final_video}")
```

## 🧪 Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/
```

### Code Quality

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **pytest** for testing

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Sarang Sapre**
- Email: sarang.sapre89@gmail.com

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## ⭐ Show your support

Give a ⭐️ if this project helped you!
