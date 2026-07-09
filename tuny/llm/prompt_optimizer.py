"""Prompt Optimization"""

from typing import Dict, Any, List

class PromptOptimizer:
    """
    Optimizes prompts for better LLM responses
    """
    
    def __init__(self):
        """Initialize optimizer"""
        self.system_prompts = {
            'code_generation': '''You are an expert code generator. 
Generate clean, efficient, well-documented code. 
Always follow best practices and include error handling.''',
            
            'code_analysis': '''You are an expert code reviewer.
Analyze code for bugs, performance issues, security vulnerabilities.
Provide clear explanations and suggestions.''',
            
            'bug_fix': '''You are an expert debugger.
Identify and fix the bug.
Explain what was wrong and why the fix works.''',
            
            'optimization': '''You are a performance optimization expert.
Analyze code for inefficiencies.
Suggest optimizations with clear explanations.'''
        }
    
    def optimize(self, prompt: str, intent: str, context: Dict[str, Any]) -> str:
        """
        Optimize prompt for better results
        
        Args:
            prompt: Original prompt
            intent: Detected intent
            context: User context and history
            
        Returns:
            Optimized prompt
        """
        # Get system prompt for intent
        system_prompt = self.system_prompts.get(intent, '')
        
        # Add context from history
        history_context = self._build_history_context(context.get('history', []))
        
        # Combine prompts
        optimized = f"""{system_prompt}

{history_context}

User Request:
{prompt}

Provide a comprehensive response with clear structure."""
        
        return optimized
    
    def _build_history_context(self, history: List[Dict]) -> str:
        """
        Build context from conversation history
        """
        if not history:
            return ""
        
        context = "Previous context:\n"
        for item in history[:3]:  # Last 3 interactions
            context += f"- {item.get('prompt', '')[:100]}...\n"
        
        return context
