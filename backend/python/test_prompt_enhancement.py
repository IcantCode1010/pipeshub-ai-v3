#!/usr/bin/env python3
"""
Simple test to verify the enhanced prompt is loaded correctly
"""
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_prompt_enhancement():
    """Test if the enhanced prompt is properly loaded"""
    try:
        from app.modules.qna.prompt_templates import qna_prompt
        
        print("Testing prompt enhancement...")
        
        # Check if the enhanced text is in the prompt
        enhanced_keywords = [
            "synthesize information from multiple documents",
            "avoid repeating the same facts", 
            "highlight any important differences or uncertainties",
            "Cite your sources clearly"
        ]
        
        prompt_found = True
        for keyword in enhanced_keywords:
            if keyword in qna_prompt:
                print(f"FOUND: '{keyword}'")
            else:
                print(f"MISSING: '{keyword}'")
                prompt_found = False
        
        if prompt_found:
            print("\nSUCCESS: Enhanced prompt is properly loaded!")
            return True
        else:
            print("\nFAILURE: Enhanced prompt is missing")
            return False
            
    except ImportError as e:
        print(f"Import error: {e}")
        return False

if __name__ == "__main__":
    test_prompt_enhancement()