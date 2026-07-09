"""Tests for TUNY Orchestrator"""

import pytest
import asyncio
from core.orchestrator import TUNYOrchestrator
from core.intent_detector import IntentDetector

@pytest.fixture
def orchestrator():
    return TUNYOrchestrator()

@pytest.fixture
def intent_detector():
    return IntentDetector()

@pytest.mark.asyncio
async def test_intent_detection(intent_detector):
    """Test intent detection"""
    intent = await intent_detector.detect("Generate a Python function to calculate fibonacci")
    assert intent == "code_generation"

@pytest.mark.asyncio
async def test_intent_image_generation(intent_detector):
    """Test image generation intent"""
    intent = await intent_detector.detect("Create a beautiful sunset image")
    assert intent == "image_generation"

def test_intent_config(intent_detector):
    """Test intent configuration"""
    config = intent_detector.get_intent_config("code_generation")
    assert config['model'] == 'llama2:70b'
    assert 'temperature' in config
