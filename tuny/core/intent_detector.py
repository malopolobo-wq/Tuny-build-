"""Intent Detection System"""

import re
from typing import Dict, Any, Optional
from enum import Enum

class Intent(Enum):
    """User intent types"""
    CODE_GENERATION = "code_generation"
    IMAGE_GENERATION = "image_generation"
    VIDEO_GENERATION = "video_generation"
    AUDIO_GENERATION = "audio_generation"
    CODE_ANALYSIS = "code_analysis"
    BUG_FIX = "bug_fix"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    CHAT = "chat"

class IntentDetector:
    """
    Detects user intent from prompts
    """
    
    def __init__(self):
        """Initialize intent detector"""
        self.keywords = {
            Intent.CODE_GENERATION: [
                'generate', 'create', 'write', 'code', 'function', 'class', 'api', 'app'
            ],
            Intent.IMAGE_GENERATION: [
                'image', 'picture', 'draw', 'create image', 'generate image', 'icon', 'logo'
            ],
            Intent.VIDEO_GENERATION: [
                'video', 'animation', 'animate', 'create video', 'motion', 'clip'
            ],
            Intent.AUDIO_GENERATION: [
                'audio', 'sound', 'voice', 'speech', 'music', 'narrate', 'tts'
            ],
            Intent.CODE_ANALYSIS: [
                'analyze', 'review', 'check', 'explain', 'understand', 'what does'
            ],
            Intent.BUG_FIX: [
                'bug', 'error', 'fix', 'broken', 'crash', 'not working', 'issue'
            ],
            Intent.OPTIMIZATION: [
                'optimize', 'performance', 'speed', 'efficient', 'improve', 'refactor'
            ],
            Intent.TESTING: [
                'test', 'unit test', 'integration test', 'coverage', 'pytest', 'jest'
            ],
            Intent.DOCUMENTATION: [
                'document', 'docs', 'readme', 'comment', 'explain', 'tutorial'
            ],
            Intent.DEPLOYMENT: [
                'deploy', 'docker', 'kubernetes', 'ci/cd', 'github actions', 'build'
            ]
        }
    
    async def detect(self, prompt: str) -> str:
        """
        Detect user intent from prompt
        
        Args:
            prompt: User input text
            
        Returns:
            Intent name as string
        """
        prompt_lower = prompt.lower()
        
        # Score each intent
        scores = {}
        for intent, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            scores[intent] = score
        
        # Return intent with highest score
        best_intent = max(scores, key=scores.get)
        return best_intent.value if scores[best_intent] > 0 else Intent.CHAT.value
    
    def get_intent_config(self, intent: str) -> Dict[str, Any]:
        """
        Get configuration for specific intent
        """
        configs = {
            Intent.CODE_GENERATION.value: {
                'model': 'llama2:70b',
                'temperature': 0.3,
                'max_tokens': 2048,
                'system_prompt': 'You are a world-class code generation expert.'
            },
            Intent.IMAGE_GENERATION.value: {
                'model': 'stable-diffusion',
                'temperature': 0.7,
                'max_tokens': 1024,
            },
            Intent.CODE_ANALYSIS.value: {
                'model': 'llama2:70b',
                'temperature': 0.2,
                'max_tokens': 1024,
            },
            Intent.BUG_FIX.value: {
                'model': 'llama2:70b',
                'temperature': 0.2,
                'max_tokens': 2048,
                'system_prompt': 'You are an expert debugger. Find and fix the bug.'
            },
        }
        return configs.get(intent, {'model': 'llama2:70b', 'temperature': 0.5})
