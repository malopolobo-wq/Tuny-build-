"""Code Optimizer"""

import re
from typing import Dict, List, Any

class CodeOptimizer:
    """
    Suggest code optimizations
    """
    
    def __init__(self):
        """Initialize optimizer"""
        self.optimizations = []
    
    async def optimize(self, code: str, language: str) -> dict:
        """
        Analyze code and suggest optimizations
        
        Args:
            code: Code to optimize
            language: Programming language
            
        Returns:
            List of optimization suggestions
        """
        try:
            if language == 'python':
                return await self._optimize_python(code)
            elif language == 'javascript':
                return await self._optimize_javascript(code)
            else:
                return {'success': False, 'error': f'Language {language} not supported'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _optimize_python(self, code: str) -> dict:
        """
        Suggest Python optimizations
        """
        suggestions = []
        lines = code.split('\n')
        
        # Check for common inefficiencies
        for i, line in enumerate(lines, 1):
            # List concatenation in loop
            if 'append' in line and 'for' in code.split(line)[0]:
                suggestions.append({
                    'line': i,
                    'type': 'performance',
                    'current': line.strip(),
                    'suggestion': 'Use list comprehension instead of append in loop',
                    'impact': 'medium'
                })
            
            # String concatenation in loop
            if '+=' in line and '"' in line:
                suggestions.append({
                    'line': i,
                    'type': 'performance',
                    'current': line.strip(),
                    'suggestion': 'Use list + join() instead of += for strings',
                    'impact': 'high'
                })
            
            # Double iteration
            if line.strip().startswith('for'):
                indent = len(line) - len(line.lstrip())
                next_lines = '\n'.join(lines[i:i+5])
                if next_lines.count('for') > 1:
                    suggestions.append({
                        'line': i,
                        'type': 'performance',
                        'current': 'Nested loops detected',
                        'suggestion': 'Consider using itertools.product() or zip()',
                        'impact': 'medium'
                    })
        
        return {
            'success': True,
            'language': 'python',
            'suggestions': suggestions[:10],
            'total_suggestions': len(suggestions)
        }
    
    async def _optimize_javascript(self, code: str) -> dict:
        """
        Suggest JavaScript optimizations
        """
        suggestions = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # var instead of const/let
            if re.search(r'\bvar\s+', line):
                suggestions.append({
                    'line': i,
                    'type': 'best-practice',
                    'current': line.strip(),
                    'suggestion': 'Use const/let instead of var',
                    'impact': 'high'
                })
            
            # == instead of ===
            if '==' in line and '===' not in line:
                suggestions.append({
                    'line': i,
                    'type': 'best-practice',
                    'current': line.strip(),
                    'suggestion': 'Use === instead of ==',
                    'impact': 'high'
                })
            
            # Array forEach with index - should use map
            if '.forEach' in line and '=>' in line:
                suggestions.append({
                    'line': i,
                    'type': 'performance',
                    'current': line.strip(),
                    'suggestion': 'Use .map() if you need the transformed array',
                    'impact': 'low'
                })
        
        return {
            'success': True,
            'language': 'javascript',
            'suggestions': suggestions[:10],
            'total_suggestions': len(suggestions)
        }
