"""
Unified AI client that supports multiple providers (OpenAI, Google Gemini).
Provides a consistent interface for text generation across different AI services.
"""

from typing import Optional, List, Dict, Any
from openai import OpenAI
import google.generativeai as genai

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
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = settings.GEMINI_MODEL
            self.client = None  # Gemini uses module-level functions
        elif self.provider == "openai":
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def generate_text(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using the configured AI provider.
        
        Args:
            prompt: The user prompt/question
            system_message: Optional system message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-1)
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Generated text response
        """
        if self.provider == "gemini":
            return self._generate_gemini(prompt, system_message, temperature, **kwargs)
        elif self.provider == "openai":
            return self._generate_openai(prompt, system_message, max_tokens, temperature, **kwargs)
    
    def _generate_gemini(
        self,
        prompt: str,
        system_message: Optional[str],
        temperature: float,
        **kwargs
    ) -> str:
        """Generate text using Google Gemini."""
        model = genai.GenerativeModel(self.model)
        
        # Combine system message and prompt for Gemini
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"
        
        # Configure generation parameters
        generation_config = {
            "temperature": temperature,
        }
        generation_config.update(kwargs)
        
        response = model.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        
        return response.text
    
    def _generate_openai(
        self,
        prompt: str,
        system_message: Optional[str],
        max_tokens: Optional[int],
        temperature: float,
        **kwargs
    ) -> str:
        """Generate text using OpenAI."""
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        # Build API parameters
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
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Multi-turn chat interface.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            temperature: Sampling temperature
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Assistant's response
        """
        if self.provider == "gemini":
            # Convert messages to Gemini format
            model = genai.GenerativeModel(self.model)
            chat = model.start_chat(history=[])
            
            # Send all messages except the last one as history
            for msg in messages[:-1]:
                if msg["role"] == "user":
                    chat.send_message(msg["content"])
            
            # Send the last message and get response
            response = chat.send_message(
                messages[-1]["content"],
                generation_config={"temperature": temperature, **kwargs}
            )
            return response.text
            
        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                **kwargs
            )
            return response.choices[0].message.content
