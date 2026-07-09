"""TUNY Orchestrator - Main AI Engine"""

import json
from typing import Dict, List, Any, Optional
from core.intent_detector import IntentDetector
from core.memory_system import MemorySystem
from llm.ollama_client import OllamaClient
from llm.prompt_optimizer import PromptOptimizer
from core.exceptions import IntentDetectionError, CodeGenerationError

class TUNYOrchestrator:
    """
    Main orchestrator that coordinates all TUNY components
    """
    
    def __init__(self):
        """Initialize orchestrator"""
        self.intent_detector = IntentDetector()
        self.memory = MemorySystem()
        self.ollama = OllamaClient()
        self.prompt_optimizer = PromptOptimizer()
        
        print("✓ TUNY Orchestrator initialized")
    
    async def process_prompt(self, prompt: str, user_id: str) -> Dict[str, Any]:
        """
        Main entry point - process user prompt
        
        Args:
            prompt: User input
            user_id: User identifier
            
        Returns:
            Response with analysis, plan, and generated code
        """
        try:
            # Step 1: Detect intent
            intent = await self.intent_detector.detect(prompt)
            
            # Step 2: Retrieve context from memory
            context = self.memory.get_context(user_id)
            
            # Step 3: Optimize prompt
            optimized_prompt = self.prompt_optimizer.optimize(
                prompt, 
                intent, 
                context
            )
            
            # Step 4: Get LLM response
            llm_response = await self.ollama.generate(
                prompt=optimized_prompt,
                model='llama2:70b'
            )
            
            # Step 5: Parse and structure response
            structured_response = self._parse_response(llm_response, intent)
            
            # Step 6: Save to memory
            self.memory.save(
                user_id=user_id,
                prompt=prompt,
                response=structured_response,
                intent=intent
            )
            
            return {
                'success': True,
                'intent': intent,
                'analysis': structured_response.get('analysis'),
                'plan': structured_response.get('plan'),
                'code': structured_response.get('code'),
                'suggestions': structured_response.get('suggestions')
            }
            
        except Exception as e:
            raise CodeGenerationError(f"Orchestration failed: {str(e)}")
    
    def _parse_response(self, response: str, intent: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format
        """
        try:
            # Try to parse as JSON if possible
            if response.strip().startswith('{'):
                return json.loads(response)
            else:
                # Otherwise structure the response
                return {
                    'analysis': response[:500],
                    'plan': self._extract_plan(response),
                    'code': self._extract_code(response),
                    'suggestions': self._extract_suggestions(response)
                }
        except Exception:
            return {
                'analysis': response,
                'plan': [],
                'code': '',
                'suggestions': []
            }
    
    def _extract_plan(self, response: str) -> List[str]:
        """Extract action plan from response"""
        # Simple extraction - can be improved with better parsing
        lines = response.split('\n')
        plan = [line.strip() for line in lines if line.strip().startswith(('-', '•', '1.', '2.', '3.'))]
        return plan[:5]  # Return top 5 steps
    
    def _extract_code(self, response: str) -> str:
        """Extract code from response"""
        if '```' in response:
            parts = response.split('```')
            return parts[1] if len(parts) > 1 else ''
        return ''
    
    def _extract_suggestions(self, response: str) -> List[str]:
        """Extract suggestions from response"""
        # Extract improvement suggestions
        suggestions = []
        lines = response.split('\n')
        for i, line in enumerate(lines):
            if 'suggest' in line.lower() or 'recommend' in line.lower():
                suggestions.append(line.strip())
        return suggestions[:3]

# Global instance
orchestrator = TUNYOrchestrator()
