"""Bug Detection and Analysis"""

import re
from typing import Dict, List, Any
from enum import Enum

class BugSeverity(Enum):
    """Bug severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class BugDetector:
    """
    Detect potential bugs in code
    """
    
    def __init__(self):
        """Initialize bug detector"""
        self.patterns = {
            'python': {
                'sql_injection': {
                    'pattern': r'execute\s*\(\s*["\'].*%s.*["\']',
                    'severity': BugSeverity.CRITICAL,
                    'message': 'SQL Injection vulnerability - use parameterized queries',
                    'suggestion': 'Use cursor.execute(query, params) with placeholders'
                },
                'hardcoded_credentials': {
                    'pattern': r'(password|api_key|secret)\s*=\s*["\']\w+["\']',
                    'severity': BugSeverity.CRITICAL,
                    'message': 'Hardcoded credentials found',
                    'suggestion': 'Use environment variables or secrets manager'
                },
                'unsafe_pickle': {
                    'pattern': r'pickle\.load|pickle\.loads',
                    'severity': BugSeverity.HIGH,
                    'message': 'Unsafe pickle usage - can execute arbitrary code',
                    'suggestion': 'Use json or other safe serialization'
                },
                'exception_too_broad': {
                    'pattern': r'except\s*:\s*$',
                    'severity': BugSeverity.MEDIUM,
                    'message': 'Bare except clause catches all exceptions',
                    'suggestion': 'Catch specific exceptions: except ValueError:'
                },
                'mutable_default': {
                    'pattern': r'def\s+\w+\([^)]*=\s*\[\]|def\s+\w+\([^)]*=\s*\{\}',
                    'severity': BugSeverity.MEDIUM,
                    'message': 'Mutable default argument',
                    'suggestion': 'Use None and create list/dict inside function'
                }
            },
            'javascript': {
                'xss_vulnerability': {
                    'pattern': r'innerHTML\s*=|dangerouslySetInnerHTML',
                    'severity': BugSeverity.CRITICAL,
                    'message': 'XSS vulnerability - innerHTML can execute scripts',
                    'suggestion': 'Use textContent or React safe methods like JSX'
                },
                'eval_usage': {
                    'pattern': r'\beval\s*\(',
                    'severity': BugSeverity.CRITICAL,
                    'message': 'eval() usage - security risk',
                    'suggestion': 'Avoid eval, use Function constructor or alternatives'
                },
                'console_left_in': {
                    'pattern': r'console\.(log|error|warn)\(',
                    'severity': BugSeverity.LOW,
                    'message': 'console.* statement left in code',
                    'suggestion': 'Remove debug statements before production'
                },
                'memory_leak': {
                    'pattern': r'addEventListener.*\(.*=>.*\)',
                    'severity': BugSeverity.MEDIUM,
                    'message': 'Potential memory leak - no removeEventListener',
                    'suggestion': 'Add removeEventListener in cleanup'
                }
            }
        }
    
    async def detect(self, code: str, language: str) -> dict:
        """
        Detect bugs in code
        
        Args:
            code: Code to analyze
            language: Programming language (python, javascript)
            
        Returns:
            List of detected bugs with severity and suggestions
        """
        try:
            bugs = []
            
            if language not in self.patterns:
                return {'success': False, 'error': f'Language {language} not supported'}
            
            patterns = self.patterns[language]
            lines = code.split('\n')
            
            # Check each pattern
            for bug_type, bug_config in patterns.items():
                pattern = bug_config['pattern']
                
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line):
                        bugs.append({
                            'type': bug_type,
                            'line': line_num,
                            'code': line.strip(),
                            'severity': bug_config['severity'].value,
                            'message': bug_config['message'],
                            'suggestion': bug_config['suggestion']
                        })
            
            # Sort by severity
            severity_order = {
                'critical': 0,
                'high': 1,
                'medium': 2,
                'low': 3
            }
            bugs.sort(key=lambda x: severity_order.get(x['severity'], 99))
            
            return {
                'success': True,
                'language': language,
                'bugs': bugs,
                'total_bugs': len(bugs),
                'critical_count': len([b for b in bugs if b['severity'] == 'critical']),
                'high_count': len([b for b in bugs if b['severity'] == 'high']),
                'risk_level': self._calculate_risk_level(bugs)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _calculate_risk_level(self, bugs: List[Dict]) -> str:
        """
        Calculate overall risk level
        """
        critical_count = len([b for b in bugs if b['severity'] == 'critical'])
        high_count = len([b for b in bugs if b['severity'] == 'high'])
        
        if critical_count > 0:
            return 'CRITICAL'
        elif high_count > 2:
            return 'HIGH'
        elif high_count > 0:
            return 'MEDIUM'
        else:
            return 'LOW'
