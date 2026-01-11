
import unittest
from unittest.mock import MagicMock
import shutil
import os
from pathlib import Path
from ai_media_orchestrator.modules.script_generator import ScriptGenerator
import ai_media_orchestrator.config
from ai_media_orchestrator.config import settings

class TestScriptGeneratorCleanup(unittest.TestCase):
    def setUp(self):
        if not settings.SCRIPTS_DIR.exists():
            settings.SCRIPTS_DIR.mkdir(parents=True)
            
    def test_double_split_cleanup(self):
        # Mock the AI client to return the problematic output seen in the logs
        dirty_output = """Here's the output in exactly TWO sections separated by ---SPLIT---

The AI revolution isn't just about robots anymore.
---SPLIT---
machine learning, business
"""
        
        generator = ScriptGenerator(provider="openai")
        generator.ai_client.generate_text = MagicMock(return_value=dirty_output)
        
        script, keywords = generator.generate_script("AI Topic", duration=10)
        
        expected_script = "The AI revolution isn't just about robots anymore."
        
        # Verify strict equality - the intro should be gone
        self.assertEqual(script.strip(), expected_script)
        
        # Verify keywords extracted correctly
        self.assertEqual(keywords, ["machine learning", "business"])

if __name__ == '__main__':
    unittest.main()
