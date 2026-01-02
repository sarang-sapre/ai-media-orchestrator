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
│       ├── core/              # Core orchestration logic
│       ├── generators/        # Content generation modules
│       ├── processors/        # Media processing utilities
│       ├── utils/             # Helper functions and utilities
│       └── config/            # Configuration management
├── tests/                     # Test suite
├── examples/                  # Example scripts and usage
├── docs/                      # Documentation
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

```python
from ai_media_orchestrator import Orchestrator

# Initialize the orchestrator
orchestrator = Orchestrator()

# Your automation workflow here
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
