"""Automatic Test Generation"""

import re
from typing import Dict, List, Any

class TestGenerator:
    """
    Generate unit tests from code
    """
    
    def __init__(self):
        """Initialize test generator"""
        pass
    
    async def generate_tests(self, code: str, language: str, 
                           test_framework: str = 'auto') -> dict:
        """
        Generate unit tests from code
        
        Args:
            code: Source code
            language: Programming language
            test_framework: Test framework (pytest, jest, etc)
            
        Returns:
            Generated test code
        """
        try:
            if language == 'python':
                return await self._generate_python_tests(code, test_framework)
            elif language == 'javascript':
                return await self._generate_javascript_tests(code, test_framework)
            else:
                return {'success': False, 'error': f'Language {language} not supported'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _generate_python_tests(self, code: str, framework: str) -> dict:
        """
        Generate Python tests (pytest)
        """
        try:
            # Extract functions and classes
            functions = self._extract_python_functions(code)
            classes = self._extract_python_classes(code)
            
            test_code = 'import pytest\n\n'
            
            # Generate tests for functions
            for func in functions:
                test_code += self._generate_function_test(func)
                test_code += '\n'
            
            # Generate tests for classes
            for cls in classes:
                test_code += self._generate_class_test(cls)
                test_code += '\n'
            
            return {
                'success': True,
                'language': 'python',
                'framework': 'pytest',
                'test_code': test_code,
                'functions_tested': len(functions),
                'classes_tested': len(classes)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _generate_javascript_tests(self, code: str, framework: str) -> dict:
        """
        Generate JavaScript tests (Jest)
        """
        try:
            # Extract functions
            functions = self._extract_js_functions(code)
            
            test_code = "import { describe, it, expect } from 'jest';\n\n"
            
            for func in functions:
                test_code += self._generate_js_function_test(func)
                test_code += '\n'
            
            return {
                'success': True,
                'language': 'javascript',
                'framework': 'jest',
                'test_code': test_code,
                'functions_tested': len(functions)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _extract_python_functions(self, code: str) -> List[Dict]:
        """
        Extract function definitions from Python code
        """
        functions = []
        pattern = r'def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*([^:]+))?:'
        
        for match in re.finditer(pattern, code):
            functions.append({
                'name': match.group(1),
                'args': match.group(2).split(',') if match.group(2) else [],
                'return_type': match.group(3)
            })
        
        return functions
    
    def _extract_python_classes(self, code: str) -> List[Dict]:
        """
        Extract class definitions from Python code
        """
        classes = []
        pattern = r'class\s+(\w+)(?:\(([^)]*)\))?:'
        
        for match in re.finditer(pattern, code):
            classes.append({
                'name': match.group(1),
                'parent': match.group(2)
            })
        
        return classes
    
    def _extract_js_functions(self, code: str) -> List[Dict]:
        """
        Extract function definitions from JavaScript
        """
        functions = []
        
        # Named functions
        pattern = r'function\s+(\w+)\s*\(([^)]*)\)|const\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>'
        
        for match in re.finditer(pattern, code):
            name = match.group(1) or match.group(3)
            args = (match.group(2) or match.group(4)).split(',') if (match.group(2) or match.group(4)) else []
            functions.append({
                'name': name,
                'args': args
            })
        
        return functions
    
    def _generate_function_test(self, func: Dict) -> str:
        """
        Generate pytest test for a function
        """
        func_name = func['name']
        args = func['args']
        
        test = f"""def test_{func_name}():
    # Test basic functionality
    result = {func_name}()
    assert result is not None
    
    # TODO: Add specific test cases
    # TODO: Test edge cases
    # TODO: Test error handling
"""
        
        return test
    
    def _generate_class_test(self, cls: Dict) -> str:
        """
        Generate pytest test for a class
        """
        class_name = cls['name']
        
        test = f"""class Test{class_name}:
    def setup_method(self):
        self.obj = {class_name}()
    
    def test_initialization(self):
        assert self.obj is not None
    
    # TODO: Add test methods for each method in the class
"""
        
        return test
    
    def _generate_js_function_test(self, func: Dict) -> str:
        """
        Generate Jest test for a JavaScript function
        """
        func_name = func['name']
        
        test = f"""describe('{func_name}', () => {{
  it('should work correctly', () => {{
    const result = {func_name}();
    expect(result).toBeDefined();
  }});
  
  // TODO: Add more test cases
  // TODO: Test edge cases
  // TODO: Test error scenarios
}});
"""
        
        return test
