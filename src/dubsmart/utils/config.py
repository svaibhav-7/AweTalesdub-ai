import os

# Configuration for the Audio Dubbing System

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'te': 'Telugu',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'pl': 'Polish',
    'tr': 'Turkish',
    'ru': 'Russian',
    'nl': 'Dutch',
    'cs': 'Czech',
    'ar': 'Arabic',
    'zh-cn': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'te': 'Telugu'
}

# Audio processing settings
AUDIO_SETTINGS = {
    'sample_rate': 16000,
    'channels': 1,
    'format': 'wav',
    'bit_depth': 16
}

# AI Model Settings
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'base')
TRANSLATION_METHOD = os.getenv('TRANSLATION_METHOD', 'nllb')
TTS_ENGINE = os.getenv('TTS_ENGINE', 'coqui')

# Voice mapping per language and speaker
VOICE_MAPPING = {
    'en': {
        'S1': {'gender': 'male', 'name': 'en-us', 'variant': 'default'},
        'S2': {'gender': 'female', 'name': 'en-au', 'variant': 'default'},
    },
    'hi': {
        'S1': {'gender': 'male', 'name': 'hi-in', 'variant': 'default'},
        'S2': {'gender': 'female', 'name': 'hi-in', 'variant': 'default'},
    },
    'te': {
        'S1': {'gender': 'male', 'name': 'te-in', 'variant': 'default'},
        'S2': {'gender': 'female', 'name': 'te-in', 'variant': 'default'},
    },
    # Add more mappings as needed
}

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Ensure directories exist
for d in [OUTPUT_DIR, TEMP_DIR, MODELS_DIR]:
    os.makedirs(d, exist_ok=True)

# Prosody and timing settings
PROSODY_SETTINGS = {
    'speed_range': (0.8, 1.2),
    'preserve_timing': True,
}

# API Keys (set as env vars)
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')
