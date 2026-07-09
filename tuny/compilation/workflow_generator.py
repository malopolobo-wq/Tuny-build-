"""GitHub Actions CI/CD Workflow Generator"""

import yaml
import os
from typing import Dict, List, Any

class WorkflowGenerator:
    """
    Generate GitHub Actions workflows for CI/CD
    """
    
    def __init__(self):
        """Initialize workflow generator"""
        self.workflows_dir = '.github/workflows'
        os.makedirs(self.workflows_dir, exist_ok=True)
    
    def generate_compile_workflow(self, languages: List[str], 
                                 platforms: List[str] = ['linux', 'windows', 'macos']) -> str:
        """
        Generate workflow for multi-language compilation
        """
        jobs = {}
        
        # Create job for each language-platform combination
        for language in languages:
            for platform in platforms:
                job_name = f'compile_{language}_{platform}'.replace('-', '_')
                
                jobs[job_name] = self._get_job_config(language, platform)
        
        workflow = {
            'name': 'TUNY Multi-Language Compilation',
            'on': {
                'push': {'branches': ['main', 'development']},
                'pull_request': {'branches': ['main', 'development']},
                'workflow_dispatch': {}
            },
            'jobs': jobs
        }
        
        return yaml.dump(workflow, default_flow_style=False)
    
    def _get_job_config(self, language: str, platform: str) -> Dict[str, Any]:
        """
        Get job configuration for language-platform combination
        """
        os_map = {
            'linux': 'ubuntu-latest',
            'windows': 'windows-latest',
            'macos': 'macos-latest'
        }
        
        runs_on = os_map.get(platform, 'ubuntu-latest')
        
        steps = [
            {'uses': 'actions/checkout@v3'},
            {'name': 'Setup environment', 'run': self._setup_command(language)},
            {'name': f'Compile {language}', 'run': self._compile_command(language)},
            {'name': 'Upload artifacts', 'uses': 'actions/upload-artifact@v3',
             'with': {'name': f'{language}-{platform}', 'path': 'data/compiled_binaries/'}}
        ]
        
        return {
            'runs-on': runs_on,
            'steps': steps
        }
    
    def _setup_command(self, language: str) -> str:
        """
        Generate setup commands for language
        """
        commands = {
            'python': 'pip install pyinstaller',
            'javascript': 'npm install -g pkg',
            'cpp': 'apt-get update && apt-get install -y build-essential',
            'java': 'apt-get install -y default-jdk',
            'kotlin': 'apt-get install -y kotlin',
            'go': 'apt-get install -y golang',
            'rust': 'curl --proto \'=https\' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y',
            'swift': 'apt-get install -y swift'
        }
        return commands.get(language, 'echo "Setup complete"')
    
    def _compile_command(self, language: str) -> str:
        """
        Generate compile commands for language
        """
        commands = {
            'python': 'pyinstaller --onefile tuny/app.py -o data/compiled_binaries',
            'javascript': 'pkg tuny/app.js -o data/compiled_binaries/app',
            'cpp': 'g++ -O3 tuny/app.cpp -o data/compiled_binaries/app',
            'java': 'javac tuny/app.java -d data/compiled_binaries',
            'go': 'go build -o data/compiled_binaries/app tuny/app.go',
            'rust': 'cargo build --release --manifest-path tuny/Cargo.toml'
        }
        return commands.get(language, 'echo "Compilation complete"')
    
    def generate_test_workflow(self) -> str:
        """
        Generate workflow for running tests
        """
        workflow = {
            'name': 'TUNY Tests',
            'on': ['push', 'pull_request'],
            'jobs': {
                'test': {
                    'runs-on': 'ubuntu-latest',
                    'strategy': {
                        'matrix': {
                            'python-version': ['3.9', '3.10', '3.11']
                        }
                    },
                    'steps': [
                        {'uses': 'actions/checkout@v3'},
                        {'uses': 'actions/setup-python@v4',
                         'with': {'python-version': '${{ matrix.python-version }}'}},
                        {'run': 'pip install -r tuny/requirements.txt'},
                        {'run': 'cd tuny && python -m pytest'},
                        {'run': 'cd tuny-build && npm install && npm run test'}
                    ]
                }
            }
        }
        return yaml.dump(workflow, default_flow_style=False)
    
    def save_workflow(self, name: str, content: str) -> str:
        """
        Save workflow to file
        """
        file_path = os.path.join(self.workflows_dir, f'{name}.yml')
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path
