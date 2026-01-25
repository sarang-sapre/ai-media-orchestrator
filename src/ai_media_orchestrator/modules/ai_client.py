"""
Unified AI client that supports multiple providers (OpenAI, Google Gemini).
Provides a consistent interface for text generation across different AI services.
"""

from typing import Optional, List, Dict
import logging
from openai import OpenAI
from google import genai
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logging.warning("tiktoken not available. Token counting will use estimation.")

from ai_media_orchestrator.config import settings

logger = logging.getLogger(__name__)


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
        self._initialize_tokenizer()

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

    def _initialize_tokenizer(self):
        """Initialize the tokenizer for token counting."""
        self.tokenizer = None
        if TIKTOKEN_AVAILABLE and self.provider in ["openai", "ollama"]:
            try:
                # Try to get encoding for the specific model
                self.tokenizer = tiktoken.encoding_for_model(self.model)
            except KeyError:
                # Fallback to cl100k_base encoding (used by gpt-4, gpt-3.5-turbo)
                logger.warning(f"No tokenizer found for model {self.model}, using cl100k_base")
                self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string.
        
        Args:
            text: The text to count tokens for
            
        Returns:
            Number of tokens (estimated if tiktoken not available)
        """
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Rough estimation: ~4 characters per token
            return len(text) // 4

    def count_message_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Count tokens in a list of messages.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Total number of tokens including message formatting overhead
        """
        if not self.tokenizer:
            # Rough estimation
            total = sum(len(msg.get("content", "")) for msg in messages) // 4
            return total + len(messages) * 4  # Add overhead per message
        
        # OpenAI format token counting
        # Based on: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # Every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(self.tokenizer.encode(str(value)))
                if key == "name":  # If there's a name, the role is omitted
                    num_tokens -= 1  # Role is always required and always 1 token
        
        num_tokens += 2  # Every reply is primed with <im_start>assistant
        return num_tokens

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

        # Count and log tokens
        token_count = self.count_tokens(contents)
        logger.info(f"[{self.provider}] Sending request with ~{token_count} input tokens")

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

        # Count and log tokens
        token_count = self.count_message_tokens(messages)
        logger.info(f"[{self.provider}] Sending request with ~{token_count} input tokens")

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

            # Count and log tokens
            token_count = self.count_tokens(prompt_text)
            logger.info(f"[{self.provider}] Sending chat request with ~{token_count} input tokens")

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt_text,
            )
            return response.text

        if self.provider in ["openai", "ollama"]:
            # Count and log tokens
            token_count = self.count_message_tokens(messages)
            logger.info(f"[{self.provider}] Sending chat request with ~{token_count} input tokens")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                **kwargs,
            )
            return response.choices[0].message.content

        raise ValueError(f"Unsupported provider: {self.provider}")
