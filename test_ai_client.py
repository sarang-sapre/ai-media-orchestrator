"""
Test script for the unified AI Client.
Verifies that the client correctly handles provider selection and text generation.
"""
import os
import sys
from dotenv import load_dotenv
from ai_media_orchestrator.modules.ai_client import AIClient
from ai_media_orchestrator.config import settings

def test_ai_client():
    print("=" * 60)
    print("Unified AI Client Test")
    print("=" * 60)
    
    # Check what's configured
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    provider = os.getenv("AI_PROVIDER", "auto")
    
    print(f"Configuration:")
    print(f"  - AI_PROVIDER: {provider}")
    print(f"  - GEMINI_API_KEY: {'[Configured]' if gemini_key else '[Missing]'}")
    print(f"  - OPENAI_API_KEY: {'[Configured]' if openai_key else '[Missing]'}")
    
    try:
        # 1. Initialize Client
        print("\n1. Initializing AI Client...")
        client = AIClient()
        print(f"  ✓ Client initialized with provider: {client.provider.upper()}")
        
        # 2. Test Text Generation
        print("\n2. Testing Text Generation...")
        prompt = "Write a one-sentence haiku about coding."
        print(f"  Request: '{prompt}'")
        
        response = client.generate_text(
            prompt=prompt,
            temperature=0.7
        )
        
        print(f"  ✓ Response received:")
        print(f"    \"{response.strip()}\"")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Test failed!")
        print(f"   Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_ai_client()
    print("=" * 60)
    exit(0 if success else 1)
