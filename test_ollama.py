"""
Test script for Ollama integration.
"""
import os
import sys

# Force AI_PROVIDER to ollama for this test
os.environ["AI_PROVIDER"] = "ollama"

from ai_media_orchestrator.modules.ai_client import AIClient
from ai_media_orchestrator.config import settings

def test_ollama():
    print("=" * 60)
    print("Ollama Integration Test")
    print("=" * 60)
    
    print(f"Configurations:")
    print(f"  - AI_PROVIDER: {settings.AI_PROVIDER}")
    print(f"  - OLLAMA_BASE_URL: {settings.OLLAMA_BASE_URL}")
    print(f"  - OLLAMA_MODEL: {settings.OLLAMA_MODEL}")
    
    try:
        print("\n1. Initializing Client...")
        client = AIClient()
        print(f"  ✓ Client initialized with provider: {client.provider}")
        
        print("\n2. Testing Generation (Expect connection error if Ollama is not running)...")
        response = client.generate_text("Say 'Hello from Ollama' if you can hear me.")
        print(f"\n  ✓ Response received:\n{response}")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed (Expected if Ollama is not running).")
        print(f"Error: {e}")
        print("\nNOTE: Make sure Ollama is installed and running ('ollama serve').")
        print("Required model must be pulled: 'ollama pull llama3'")
        return False

if __name__ == "__main__":
    test_ollama()
