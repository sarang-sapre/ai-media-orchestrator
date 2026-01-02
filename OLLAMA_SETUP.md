# Ollama Setup Guide

This guide explains how to set up and use Ollama as a local AI provider for the AI Media Orchestrator.

## 1. Install Ollama

Download and install Ollama from the official website: [https://ollama.com/](https://ollama.com/)

## 2. Pull the Model

Open your terminal or command prompt and pull the Llama 3 model (or your preferred model):

```bash
ollama pull llama3
```

To verify it's running, you can try:

```bash
ollama run llama3 "Hello, are you working?"
```

(Type `/bye` to exit the chat)

## 3. Configure the Project

You can configure the orchestrator to use Ollama in two ways:

### Method A: Explicit Configuration (Recommended)

Add these lines to your `.env` file:

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3
```

### Method B: Auto-Detection fallback

If `AI_PROVIDER` is set to `auto` (default) and no other API keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`) are present, the system will automatically fall back to trying Ollama.

## 4. Run the Orchestrator

Run the application as usual:

```bash
python src/ai_media_orchestrator/main.py
```

It should show `Active Provider: OLLAMA` in the startup logs.
