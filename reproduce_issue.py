
import sys
from ai_media_orchestrator.modules.script_generator import ScriptGenerator
from ai_media_orchestrator.config import settings

def main():
    print("DEBUG: Starting reproduction script...")
    print(f"DEBUG: Active provider: {settings.AI_PROVIDER}")
    
    # Force settings if necessary, but relying on env/defaults is better
    # We want to replicate the user's environment exactly
    
    generator = ScriptGenerator()
    topic = "AI for Business"
    
    print(f"DEBUG: Generating script for topic: '{topic}'")
    try:
        script, keywords = generator.generate_script(topic, duration=30)
        
        print("\n" + "="*50)
        print("FINAL CLEAN SCRIPT OUTPUT:")
        print("="*50)
        print(script)
        print("="*50)
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
