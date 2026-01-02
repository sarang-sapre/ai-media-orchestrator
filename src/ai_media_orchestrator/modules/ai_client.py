"""
Unified AI client that supports multiple providers (OpenAI, Google Gemini).
Provides a consistent interface for text generation across different AI services.
"""

from typing import Optional, List, Dict
from openai import OpenAI
from google import genai

from ai_media_orchestrator.config import settings


class AIClient:
    """
    Unified AI client that abstracts away provider-specific implementations.
    Supports both OpenAI and Google Gemini APIs.
    """

    def __init__(self, provider: Optional[str] = None):
        """
        Initialize the AI client with the specified or auto-detected provider.

        Args:
            provider: AI provider to use ('gemini', 'openai', or None for auto-detection)
        """
        self.provider = provider or settings.get_active_provider()
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate client based on the provider."""
        if self.provider == "gemini":
            self.client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )
            self.model = settings.GEMINI_MODEL

        elif self.provider == "openai":
            self.client = OpenAI(
                api_key=settings.OPENAI_API_KEY
            )
            self.model = settings.OPENAI_MODEL

        elif self.provider == "ollama":
            self.client = OpenAI(
                base_url=settings.OLLAMA_BASE_URL,
                api_key="ollama"  # Required by SDK but ignored by Ollama
            )
            self.model = settings.OLLAMA_MODEL

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate_text(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs,
    ) -> str:
        """
        Generate text using the configured AI provider.
        """
        if self.provider == "gemini":
            return self._generate_gemini(prompt, system_message, temperature)

        if self.provider in ["openai", "ollama"]:
            return self._generate_openai(
                prompt, system_message, max_tokens, temperature, **kwargs
            )

        raise ValueError(f"Unsupported provider: {self.provider}")

    # =========================
    # Gemini (NEW SDK – FIXED)
    # =========================
    def _generate_gemini(
        self,
        prompt: str,
        system_message: Optional[str],
        temperature: float,
    ) -> str:
        """Generate text using Google Gemini (google.genai)."""

        if system_message:
            contents = f"{system_message}\n\n{prompt}"
        else:
            contents = prompt

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
        )

        return response.text

    # =========================
    # OpenAI (unchanged)
    # =========================
    def _generate_openai(
        self,
        prompt: str,
        system_message: Optional[str],
        max_tokens: Optional[int],
        temperature: float,
        **kwargs,
    ) -> str:
        """Generate text using OpenAI."""
        messages = []

        if system_message:
            messages.append({"role": "system", "content": system_message})

        messages.append({"role": "user", "content": prompt})

        api_params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens:
            api_params["max_tokens"] = max_tokens

        api_params.update(kwargs)

        response = self.client.chat.completions.create(**api_params)
        return response.choices[0].message.content

    # =========================
    # Chat (multi-turn)
    # =========================
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        **kwargs,
    ) -> str:
        """
        Multi-turn chat interface.
        """
        if self.provider == "gemini":
            # Gemini expects a single combined prompt
            combined_prompt = []
            for msg in messages:
                role = msg["role"].upper()
                combined_prompt.append(f"{role}: {msg['content']}")

            prompt_text = "\n".join(combined_prompt)

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt_text,
            )
            return response.text

        if self.provider in ["openai", "ollama"]:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                **kwargs,
            )
            return response.choices[0].message.content

        raise ValueError(f"Unsupported provider: {self.provider}")
