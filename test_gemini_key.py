"""
Simple script to test if the Google Gemini API key is working.
"""
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

def test_gemini_api_key():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the API key
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file")
        print("Please add GEMINI_API_KEY=your_key_here to your .env file")
        return False
    
    print(f"✓ API key found (starts with: {api_key[:10]}...)")
    
    try:
        # Configure the Gemini client
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Make a simple API call to test the key
        print("\n🔄 Testing API key with a simple generation request...")
        response = model.generate_content("Say 'Gemini API is working!' if you receive this.")
        
        print(f"\n✅ SUCCESS! Gemini API responded with: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: API key test failed!")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Google Gemini API Key Test")
    print("=" * 60)
    success = test_gemini_api_key()
    print("=" * 60)
    exit(0 if success else 1)
