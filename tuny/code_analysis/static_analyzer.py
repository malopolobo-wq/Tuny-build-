"""Static Code Analysis"""

import subprocess
import json
import os
from typing import Dict, List, Any, Optional

class StaticAnalyzer:
    """
    Perform static code analysis using ESLint, Pylint, SonarQube
    """
    
    def __init__(self):
        """Initialize analyzer"""
        self.output_dir = 'data/analysis_reports'
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def analyze_python(self, code: str, file_path: str = 'temp.py') -> dict:
        """
        Analyze Python code with Pylint
        
        Args:
            code: Python code to analyze
            file_path: File path for context
            
        Returns:
            Analysis results with issues and scores
        """
        try:
            # Write code to temp file
            temp_file = f'/tmp/{file_path}'
            os.makedirs(os.path.dirname(temp_file), exist_ok=True)
            
            with open(temp_file, 'w') as f:
                f.write(code)
            
            # Run Pylint
            result = subprocess.run(
                ['pylint', temp_file, '--output-format=json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            try:
                issues = json.loads(result.stdout)
            except json.JSONDecodeError:
                issues = []
            
            # Calculate score
            score = self._calculate_quality_score(issues)
            
            # Categorize issues
            categorized = self._categorize_issues(issues)
            
            # Cleanup
            os.remove(temp_file)
            
            return {
                'success': True,
                'language': 'python',
                'score': score,
                'issues': categorized,
                'total_issues': len(issues),
                'by_type': {
                    'errors': len([i for i in issues if i.get('type') == 'error']),
                    'warnings': len([i for i in issues if i.get('type') == 'warning']),
                    'convention': len([i for i in issues if i.get('type') == 'convention']),
                    'refactor': len([i for i in issues if i.get('type') == 'refactor'])
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def analyze_javascript(self, code: str, file_path: str = 'temp.js') -> dict:
        """
        Analyze JavaScript/TypeScript code with ESLint
        """
        try:
            # Write code to temp file
            temp_file = f'/tmp/{file_path}'
            os.makedirs(os.path.dirname(temp_file), exist_ok=True)
            
            with open(temp_file, 'w') as f:
                f.write(code)
            
            # Run ESLint
            result = subprocess.run(
                ['eslint', temp_file, '--format=json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            try:
                data = json.loads(result.stdout) if result.stdout else []
                issues = data[0]['messages'] if data else []
            except (json.JSONDecodeError, KeyError, IndexError):
                issues = []
            
            # Calculate score
            score = self._calculate_quality_score(issues)
            
            # Categorize issues
            categorized = self._categorize_issues(issues)
            
            # Cleanup
            os.remove(temp_file)
            
            return {
                'success': True,
                'language': 'javascript',
                'score': score,
                'issues': categorized,
                'total_issues': len(issues),
                'by_severity': {
                    'error': len([i for i in issues if i.get('severity') == 2]),
                    'warning': len([i for i in issues if i.get('severity') == 1])
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _categorize_issues(self, issues: List[Dict]) -> List[Dict]:
        """
        Categorize and prioritize issues
        """
        categorized = []
        
        for issue in issues[:20]:  # Top 20 issues
            categorized.append({
                'line': issue.get('line') or issue.get('lineno'),
                'column': issue.get('column') or issue.get('col_offset'),
                'message': issue.get('message'),
                'rule': issue.get('symbol') or issue.get('ruleId'),
                'severity': issue.get('type') or ('error' if issue.get('severity') == 2 else 'warning'),
                'suggestion': self._get_suggestion(issue)
            })
        
        return categorized
    
    def _calculate_quality_score(self, issues: List[Dict]) -> float:
        """
        Calculate code quality score (0-100)
        """
        if not issues:
            return 100.0
        
        # Weight issues by severity
        score = 100.0
        for issue in issues:
            severity = issue.get('type') or issue.get('severity')
            if severity in ['error', 2]:
                score -= 5
            elif severity in ['warning', 1]:
                score -= 2
            else:
                score -= 1
        
        return max(0, score)
    
    def _get_suggestion(self, issue: Dict) -> str:
        """
        Get fix suggestion for common issues
        """
        message = issue.get('message', '').lower()
        
        suggestions = {
            'unused': 'Remove unused variable or import',
            'undefined': 'Define variable before use',
            'trailing': 'Remove trailing whitespace',
            'quotes': 'Use consistent quote style',
            'semicolon': 'Add or remove semicolon consistently',
            'indentation': 'Fix indentation',
            'complexity': 'Reduce function complexity',
            'line too long': 'Break long lines into multiple lines'
        }
        
        for keyword, suggestion in suggestions.items():
            if keyword in message:
                return suggestion
        
        return 'Review and fix this issue'
