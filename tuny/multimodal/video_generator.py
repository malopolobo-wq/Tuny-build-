"""Video Generation with Stable Video Diffusion + Deforum"""

import os
import json
import asyncio
from typing import Optional, List, Dict, Any

class VideoGenerator:
    """
    Generate videos using Stable Video Diffusion + Deforum animation
    """
    
    def __init__(self):
        """Initialize video generator"""
        self.sd_api_url = os.getenv('SD_API_URL', 'http://localhost:7860')
        self.output_dir = 'data/generated_videos'
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_from_image(self, image_path: str, num_frames: int = 25,
                                 motion_bucket_id: int = 127,
                                 fps: int = 8) -> dict:
        """
        Generate video from static image using SVD
        
        Args:
            image_path: Path to input image
            num_frames: Number of frames to generate (15-25)
            motion_bucket_id: Motion intensity (1-255, 127 is default)
            fps: Frames per second
            
        Returns:
            Generated video metadata
        """
        try:
            import base64
            import requests
            
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Build SVD workflow
            workflow = self._build_svd_workflow(
                image_data, num_frames, motion_bucket_id
            )
            
            response = requests.post(
                f"{self.sd_api_url}/prompt",
                json=workflow,
                timeout=600
            )
            
            if response.status_code != 200:
                raise Exception(f"Video generation failed: {response.text}")
            
            result = response.json()
            prompt_id = result.get('prompt_id')
            
            # Wait for completion
            video_data = await self._wait_for_video(prompt_id)
            
            return {
                'success': True,
                'video': video_data,
                'frames': num_frames,
                'fps': fps,
                'duration': num_frames / fps
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def generate_animation(self, prompt: str, num_frames: int = 60,
                                animation_type: str = 'camera_zoom',
                                **kwargs) -> dict:
        """
        Generate animated video using Deforum
        
        Args:
            prompt: Animation description
            num_frames: Total frames
            animation_type: Type of animation (camera_zoom, pan, etc)
            
        Returns:
            Generated animation metadata
        """
        try:
            # Build Deforum settings
            deforum_config = self._build_deforum_config(
                prompt, num_frames, animation_type, **kwargs
            )
            
            # Generate animation frames
            frames = []
            for frame_num in range(num_frames):
                frame_config = self._get_frame_config(
                    deforum_config, frame_num, num_frames
                )
                
                # Generate frame
                frame = await self._generate_frame(frame_config)
                frames.append(frame)
            
            # Combine frames into video
            video_path = await self._create_video_from_frames(
                frames, num_frames=num_frames
            )
            
            return {
                'success': True,
                'video': video_path,
                'frames': num_frames,
                'duration': num_frames / 30
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _build_svd_workflow(self, image_data: str, num_frames: int,
                           motion_bucket_id: int) -> dict:
        """
        Build ComfyUI workflow for SVD video generation
        """
        return {
            "1": {
                "inputs": {
                    "ckpt_name": "svd_xt_1_0.safetensors"
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "2": {
                "inputs": {
                    "image": image_data
                },
                "class_type": "LoadImage"
            },
            "3": {
                "inputs": {
                    "motion_bucket_id": motion_bucket_id,
                    "fps": 8,
                    "augmentation_level": 0,
                    "num_frames": num_frames
                },
                "class_type": "SVDVideoSampler"
            },
            "4": {
                "inputs": {
                    "filename_prefix": "TUNY_video_"
                },
                "class_type": "VHS_VideoCombine"
            }
        }
    
    def _build_deforum_config(self, prompt: str, num_frames: int,
                             animation_type: str, **kwargs) -> dict:
        """
        Build Deforum animation configuration
        """
        configs = {
            'camera_zoom': {
                'zoom_schedule': 'linear',
                'zoom_start': 1.0,
                'zoom_end': 1.5
            },
            'pan': {
                'pan_x': 'linear',
                'pan_x_start': 0,
                'pan_x_end': 100,
                'pan_y': 'sine',
                'pan_y_start': 0,
                'pan_y_end': 50
            },
            'rotation': {
                'rotation_schedule': 'linear',
                'rotation_start': 0,
                'rotation_end': 360
            }
        }
        
        base_config = configs.get(animation_type, configs['camera_zoom'])
        return {
            'prompt': prompt,
            'num_frames': num_frames,
            'animation_type': animation_type,
            **base_config,
            **kwargs
        }
    
    def _get_frame_config(self, deforum_config: dict, frame_num: int,
                         total_frames: int) -> dict:
        """
        Calculate frame-specific configuration
        """
        progress = frame_num / total_frames
        
        return {
            'prompt': deforum_config['prompt'],
            'frame_num': frame_num,
            'progress': progress,
            'seed': frame_num,
            'animation_config': deforum_config
        }
    
    async def _generate_frame(self, frame_config: dict) -> str:
        """
        Generate single animation frame
        """
        # This would use image generation with animation parameters
        await asyncio.sleep(0.1)  # Placeholder
        return f"frame_{frame_config['frame_num']:04d}.png"
    
    async def _create_video_from_frames(self, frames: List[str],
                                        num_frames: int) -> str:
        """
        Combine frames into video file
        """
        try:
            import subprocess
            
            output_path = os.path.join(self.output_dir, 'animation.mp4')
            
            # Use FFmpeg to create video
            cmd = [
                'ffmpeg',
                '-framerate', '30',
                '-i', os.path.join(self.output_dir, 'frame_%04d.png'),
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                output_path,
                '-y'
            ]
            
            # Run FFmpeg
            subprocess.run(cmd, capture_output=True, check=True)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Video creation failed: {str(e)}")
    
    async def _wait_for_video(self, prompt_id: str) -> str:
        """
        Wait for video generation to complete
        """
        import time
        import requests
        
        max_retries = 300  # 5 minutes timeout
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
                        videos = output.get('video', [])
                        if videos:
                            return videos[0].get('filename')
                
                await asyncio.sleep(2)
                retry_count += 1
                
            except Exception:
                await asyncio.sleep(2)
                retry_count += 1
        
        raise Exception("Video generation timeout")
