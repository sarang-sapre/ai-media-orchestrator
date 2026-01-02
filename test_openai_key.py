"""
Simple script to test if the OpenAI API key is working.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

def test_openai_api_key():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the API key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in .env file")
        return False
    
    print(f"✓ API key found (starts with: {api_key[:10]}...)")
    
    try:
        # Initialize the OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Make a simple API call to test the key
        print("\n🔄 Testing API key with a simple completion request...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'API key is working!' if you receive this."}
            ],
            max_tokens=20
        )
        
        result = response.choices[0].message.content
        print(f"\n✅ SUCCESS! OpenAI API responded with: {result}")
        print(f"\n📊 API Details:")
        print(f"   - Model used: {response.model}")
        print(f"   - Tokens used: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: API key test failed!")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("OpenAI API Key Test")
    print("=" * 60)
    success = test_openai_api_key()
    print("=" * 60)
    exit(0 if success else 1)
