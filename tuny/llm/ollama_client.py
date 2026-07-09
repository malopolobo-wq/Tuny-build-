"""Ollama LLM Client"""

import requests
import os
from typing import Optional, Dict, Any
from core.exceptions import OllamaConnectionError

class OllamaClient:
    """
    Client for interacting with Ollama models
    """
    
    def __init__(self, base_url: str = None):
        """Initialize Ollama client"""
        self.base_url = base_url or os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.timeout = int(os.getenv('OLLAMA_TIMEOUT', 300))
        self._verify_connection()
    
    def _verify_connection(self):
        """
        Verify connection to Ollama
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise OllamaConnectionError()
        except requests.exceptions.RequestException:
            raise OllamaConnectionError(
                f"Cannot connect to Ollama at {self.base_url}"
            )
    
    async def generate(self, prompt: str, model: str = 'llama2:70b', 
                      temperature: float = 0.5, max_tokens: int = 2048) -> str:
        """
        Generate text using Ollama
        
        Args:
            prompt: Input prompt
            model: Model name
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature,
                    "num_predict": max_tokens
                },
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama error: {response.text}")
            
            return response.json().get('response', '')
            
        except requests.exceptions.Timeout:
            raise Exception("Ollama request timeout")
        except Exception as e:
            raise Exception(f"Ollama generation failed: {str(e)}")
    
    async def stream_generate(self, prompt: str, model: str = 'llama2:70b'):
        """
        Generate text with streaming
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": True
                },
                timeout=self.timeout,
                stream=True
            )
            
            for line in response.iter_lines():
                if line:
                    yield line.decode('utf-8')
                    
        except Exception as e:
            raise Exception(f"Ollama streaming failed: {str(e)}")
    
    def list_models(self) -> list:
        """
        List available models
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.json().get('models', [])
        except Exception as e:
            raise Exception(f"Failed to list models: {str(e)}")
