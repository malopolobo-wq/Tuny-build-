"""Image Generation with Stable Diffusion"""

import requests
import base64
import os
from typing import Optional, List
from PIL import Image
from io import BytesIO

class ImageGenerator:
    """
    Generate images using Stable Diffusion
    """
    
    def __init__(self):
        """Initialize image generator"""
        self.sd_api_url = os.getenv('SD_API_URL', 'http://localhost:7860')
        self.output_dir = 'data/generated_images'
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate(self, prompt: str, negative_prompt: str = "",
                      num_inference_steps: int = 50, guidance_scale: float = 7.5,
                      width: int = 512, height: int = 512) -> dict:
        """
        Generate image from text prompt
        
        Args:
            prompt: Image description
            negative_prompt: What to avoid
            num_inference_steps: Quality steps (50-100)
            guidance_scale: Adherence to prompt (7.5 is good)
            width: Image width
            height: Image height
            
        Returns:
            Generated image data and metadata
        """
        try:
            # Use ComfyUI API
            workflow = self._build_workflow(
                prompt, negative_prompt, num_inference_steps, 
                guidance_scale, width, height
            )
            
            response = requests.post(
                f"{self.sd_api_url}/prompt",
                json=workflow,
                timeout=300
            )
            
            if response.status_code != 200:
                raise Exception(f"Generation failed: {response.text}")
            
            result = response.json()
            prompt_id = result.get('prompt_id')
            
            # Poll for result
            image_data = await self._wait_for_completion(prompt_id)
            
            return {
                'success': True,
                'image': image_data,
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'width': width,
                'height': height
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_workflow(self, prompt: str, negative_prompt: str,
                       steps: int, guidance: float, width: int, height: int) -> dict:
        """
        Build ComfyUI workflow for image generation
        """
        return {
            "1": {
                "inputs": {
                    "ckpt_name": "sd_xl_base_1.0.safetensors"
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "2": {
                "inputs": {
                    "text": prompt
                },
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "CLIP Text Encode (Prompt)"}
            },
            "3": {
                "inputs": {
                    "text": negative_prompt
                },
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "CLIP Text Encode (Negative)"}
            },
            "4": {
                "inputs": {
                    "seed": 0,
                    "steps": steps,
                    "cfg": guidance,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1
                },
                "class_type": "KSampler"
            },
            "5": {
                "inputs": {
                    "filename_prefix": "TUNY_"
                },
                "class_type": "SaveImage"
            }
        }
    
    async def _wait_for_completion(self, prompt_id: str) -> str:
        """
        Wait for image generation to complete
        """
        import time
        import asyncio
        
        max_retries = 120
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                response = requests.get(
                    f"{self.sd_api_url}/history/{prompt_id}",
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if prompt_id in result:
                        output = result[prompt_id].get('outputs', {})
                        images = output.get('images', [])
                        if images:
                            return images[0].get('filename')
                
                await asyncio.sleep(1)
                retry_count += 1
                
            except Exception as e:
                await asyncio.sleep(1)
                retry_count += 1
        
        raise Exception("Image generation timeout")
    
    async def generate_variations(self, image_path: str, num_variations: int = 4) -> dict:
        """
        Generate variations of an image (img2img)
        """
        try:
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            workflow = {
                "1": {
                    "inputs": {
                        "image": image_data
                    },
                    "class_type": "LoadImage"
                },
                "2": {
                    "inputs": {
                        "strength": 0.7,
                        "prompt": "High quality variation"
                    },
                    "class_type": "VAEDecode"
                }
            }
            
            results = []
            for i in range(num_variations):
                response = requests.post(
                    f"{self.sd_api_url}/prompt",
                    json=workflow,
                    timeout=300
                )
                results.append(response.json())
            
            return {
                'success': True,
                'variations': results,
                'count': num_variations
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
