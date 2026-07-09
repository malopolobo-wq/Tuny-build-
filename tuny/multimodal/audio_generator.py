"""Audio Generation with Bark + XTTS"""

import os
import numpy as np
from typing import Optional, Dict, Any
import asyncio

class AudioGenerator:
    """
    Generate audio and speech using Bark + XTTS
    """
    
    def __init__(self):
        """Initialize audio generator"""
        self.output_dir = 'data/generated_audio'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Try to load Bark
        try:
            from bark import SAMPLE_RATE, generate_audio, preload_models
            self.bark_available = True
            preload_models()
        except ImportError:
            self.bark_available = False
        
        # Try to load XTTS
        try:
            from TTS.api import TTS
            self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
            self.xtts_available = True
        except ImportError:
            self.xtts_available = False
    
    async def generate_speech(self, text: str, voice: str = 'default',
                             language: str = 'en') -> dict:
        """
        Generate speech from text using XTTS
        
        Args:
            text: Text to convert to speech
            voice: Voice type/preset
            language: Language code (en, fr, es, etc)
            
        Returns:
            Audio file path and metadata
        """
        try:
            if not self.xtts_available:
                return {'success': False, 'error': 'XTTS not available'}
            
            from TTS.api import TTS
            
            # Generate speech
            output_path = os.path.join(self.output_dir, f'speech_{hash(text)}.wav')
            
            self.tts.tts_to_file(
                text=text,
                speaker_wav=None,
                language=language,
                file_path=output_path
            )
            
            return {
                'success': True,
                'audio': output_path,
                'text': text,
                'voice': voice,
                'language': language
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def voice_clone(self, text: str, voice_sample_path: str) -> dict:
        """
        Generate speech with voice cloning from sample
        
        Args:
            text: Text to speak
            voice_sample_path: Path to voice sample (30+ seconds)
            
        Returns:
            Generated audio with cloned voice
        """
        try:
            if not self.xtts_available:
                return {'success': False, 'error': 'XTTS not available'}
            
            output_path = os.path.join(self.output_dir, f'cloned_voice_{hash(text)}.wav')
            
            self.tts.tts_to_file(
                text=text,
                speaker_wav=voice_sample_path,
                language='en',
                file_path=output_path
            )
            
            return {
                'success': True,
                'audio': output_path,
                'text': text,
                'cloned': True
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def generate_audio(self, text: str, voice_preset: str = "v2/en_speaker_6",
                            temperature: float = 0.8) -> dict:
        """
        Generate expressive audio using Bark
        
        Args:
            text: Text to synthesize
            voice_preset: Voice preset from Bark
            temperature: Creativity level (0.6-1.0)
            
        Returns:
            Generated audio metadata
        """
        try:
            if not self.bark_available:
                return {'success': False, 'error': 'Bark not available'}
            
            from bark import generate_audio, SAMPLE_RATE
            import scipy.io.wavfile as wavfile
            
            # Generate audio
            audio_array = generate_audio(
                text,
                history_prompt=voice_preset,
                temperature=temperature
            )
            
            # Save to file
            output_path = os.path.join(self.output_dir, f'audio_{hash(text)}.wav')
            wavfile.write(output_path, SAMPLE_RATE, audio_array)
            
            return {
                'success': True,
                'audio': output_path,
                'text': text,
                'voice_preset': voice_preset,
                'sample_rate': SAMPLE_RATE
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def generate_singing(self, lyrics: str, melody: Optional[str] = None) -> dict:
        """
        Generate singing/musical audio
        """
        try:
            if not self.bark_available:
                return {'success': False, 'error': 'Bark not available'}
            
            from bark import generate_audio, SAMPLE_RATE
            import scipy.io.wavfile as wavfile
            
            # Add music markers to text for Bark
            musical_text = f"♪ {lyrics} ♪"
            
            audio_array = generate_audio(
                musical_text,
                history_prompt="v2/en_speaker_1",
                temperature=0.9
            )
            
            output_path = os.path.join(self.output_dir, f'singing_{hash(lyrics)}.wav')
            wavfile.write(output_path, SAMPLE_RATE, audio_array)
            
            return {
                'success': True,
                'audio': output_path,
                'lyrics': lyrics,
                'type': 'singing'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def add_effects(self, audio_path: str, effect_type: str = 'reverb',
                         intensity: float = 0.5) -> dict:
        """
        Add audio effects to generated audio
        
        Args:
            audio_path: Path to audio file
            effect_type: Type of effect (reverb, echo, pitch_shift, etc)
            intensity: Effect intensity (0-1)
            
        Returns:
            Modified audio path
        """
        try:
            import librosa
            import soundfile as sf
            
            # Load audio
            y, sr = librosa.load(audio_path)
            
            # Apply effects
            if effect_type == 'reverb':
                # Simple reverb using convolution
                y = librosa.effects.preemphasis(y) if intensity > 0.5 else y
            elif effect_type == 'echo':
                # Echo effect
                delay = int(sr * intensity)
                echo = np.zeros(len(y) + delay)
                echo[:len(y)] = y
                echo[delay:] += y * (1 - intensity)
                y = echo / np.max(np.abs(echo))
            elif effect_type == 'pitch_shift':
                # Pitch shift
                steps = int(intensity * 12)  # Up to 1 octave
                y = librosa.effects.pitch_shift(y, sr=sr, n_steps=steps)
            
            # Save processed audio
            output_path = audio_path.replace('.wav', f'_{effect_type}.wav')
            sf.write(output_path, y, sr)
            
            return {
                'success': True,
                'audio': output_path,
                'effect': effect_type,
                'intensity': intensity
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
