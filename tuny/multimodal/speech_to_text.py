"""Speech-to-Text with Faster-Whisper"""

import os
from typing import Optional, Dict, Any
import asyncio

class SpeechToText:
    """
    Transcribe audio to text using Faster-Whisper
    """
    
    def __init__(self, model_size: str = 'base'):
        """
        Initialize Whisper model
        
        Args:
            model_size: Model size (tiny, base, small, medium, large)
        """
        try:
            from faster_whisper import WhisperModel
            self.model = WhisperModel(
                model_size,
                device="auto",
                compute_type="auto"
            )
            self.available = True
        except ImportError:
            self.available = False
    
    async def transcribe(self, audio_path: str, language: Optional[str] = None,
                        beam_size: int = 5) -> dict:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            language: Language code (auto-detect if None)
            beam_size: Beam search size (higher = more accurate but slower)
            
        Returns:
            Transcribed text and metadata
        """
        try:
            if not self.available:
                return {'success': False, 'error': 'Whisper not available'}
            
            if not os.path.exists(audio_path):
                return {'success': False, 'error': 'Audio file not found'}
            
            # Transcribe
            segments, info = self.model.transcribe(
                audio_path,
                language=language,
                beam_size=beam_size,
                verbose=False
            )
            
            # Combine segments
            full_text = " ".join([segment.text for segment in segments])
            
            # Extract metadata
            segment_data = [
                {
                    'text': segment.text,
                    'start': segment.start,
                    'end': segment.end,
                    'confidence': segment.confidence
                } for segment in segments
            ]
            
            return {
                'success': True,
                'text': full_text,
                'language': info.language,
                'language_probability': info.language_probability,
                'duration': info.duration,
                'segments': segment_data
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def transcribe_streaming(self, audio_stream):
        """
        Transcribe from audio stream in real-time
        """
        try:
            if not self.available:
                return {'success': False, 'error': 'Whisper not available'}
            
            # This would require handling real-time streaming
            # Placeholder for now
            return {'success': False, 'error': 'Streaming not yet implemented'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def extract_keywords(self, audio_path: str) -> dict:
        """
        Extract keywords from audio
        """
        try:
            transcription = await self.transcribe(audio_path)
            
            if not transcription['success']:
                return transcription
            
            import nltk
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            
            # Download required NLTK data
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt')
                nltk.download('stopwords')
            
            text = transcription['text'].lower()
            tokens = word_tokenize(text)
            stop_words = set(stopwords.words('english'))
            keywords = [word for word in tokens if word.isalnum() and word not in stop_words]
            
            return {
                'success': True,
                'text': transcription['text'],
                'keywords': keywords[:10]
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
