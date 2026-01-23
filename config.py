"""
Configuration settings for the Audio Dubbing System
"""
import os

# Configure ffmpeg path for pydub
# This helps pydub find ffmpeg even if it's not in the current PATH
import pydub
import os as _os
FFMPEG_DIR = _os.path.join(_os.path.dirname(__file__), 'ffmpeg-8.0.1-essentials_build', 'bin')
if _os.path.exists(_os.path.join(FFMPEG_DIR, 'ffmpeg.exe')):
    # Set for pydub
    pydub.AudioSegment.converter = _os.path.join(FFMPEG_DIR, 'ffmpeg.exe')
    pydub.AudioSegment.ffmpeg = _os.path.join(FFMPEG_DIR, 'ffmpeg.exe')
    pydub.AudioSegment.ffprobe = _os.path.join(FFMPEG_DIR, 'ffprobe.exe')
    
    # Set for other modules (like whisper) that use subprocess to call 'ffmpeg'
    if FFMPEG_DIR not in _os.environ["PATH"]:
        _os.environ["PATH"] = FFMPEG_DIR + _os.pathsep + _os.environ["PATH"]

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'te': 'Telugu',
    'es': 'Spanish'
}

# Audio processing settings
AUDIO_SETTINGS = {
    'sample_rate': 16000,  # 16kHz required for ASR
    'channels': 1,          # Mono audio
    'format': 'wav',
    'bit_depth': 16
}

# Whisper model settings
WHISPER_MODEL = 'base'  # Options: tiny, base, small, medium, large
# Use 'base' for good balance of speed and accuracy

# Translation settings
TRANSLATION_METHOD = 'm2m100'  # Options: 'm2m100', 'marian', 'google', 'gemini'

# TTS settings
TTS_ENGINE = 'coqui'  # Options: 'gtts', 'pyttsx3', 'coqui'

# Voice mapping per language and speaker
# Format: language -> speaker_id -> voice_config
VOICE_MAPPING = {
    'en': {
        'S1': {'gender': 'male', 'name': 'en-us', 'variant': 'default'},
        'S2': {'gender': 'female', 'name': 'en-au', 'variant': 'default'},
        'S3': {'gender': 'male', 'name': 'en-uk', 'variant': 'default'},
        'S4': {'gender': 'female', 'name': 'en-in', 'variant': 'default'},
    },
    'hi': {
        'S1': {'gender': 'male', 'name': 'hi-in', 'variant': 'default'},
        'S2': {'gender': 'female', 'name': 'hi-in', 'variant': 'default'},
        'S3': {'gender': 'male', 'name': 'hi-in', 'variant': 'default'},
        'S4': {'gender': 'female', 'name': 'hi-in', 'variant': 'default'},
    },
    'te': {
        'S1': {'gender': 'male', 'name': 'te-in', 'variant': 'default'},
        'S2': {'gender': 'female', 'name': 'te-in', 'variant': 'default'},
        'S3': {'gender': 'male', 'name': 'te-in', 'variant': 'default'},
        'S4': {'gender': 'female', 'name': 'te-in', 'variant': 'default'},
    },
    'es': {
        'S1': {'gender': 'male', 'name': 'es-es', 'variant': 'default'},
        'S2': {'gender': 'female', 'name': 'es-es', 'variant': 'default'},
        'S3': {'gender': 'male', 'name': 'es-mx', 'variant': 'default'},
        'S4': {'gender': 'female', 'name': 'es-mx', 'variant': 'default'},
    }
}

# Directories
OUTPUT_DIR = 'output'
TEMP_DIR = 'temp'
MODELS_DIR = 'models'

# Create directories if they don't exist
for directory in [OUTPUT_DIR, TEMP_DIR, MODELS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Noise suppression settings
NOISE_REDUCTION = {
    'algorithm': 'afftdn',  # ffmpeg noise reduction filter
    'noise_floor': -50      # dB
}

# VAD settings
VAD_SETTINGS = {
    'threshold': 0.5,       # Confidence threshold for speech detection
    'min_speech_duration': 0.25,  # Minimum speech duration in seconds
    'min_silence_duration': 0.1   # Minimum silence duration in seconds
}

# Speaker diarization settings
DIARIZATION_SETTINGS = {
    'min_speakers': 1,
    'max_speakers': 8,
    'use_pyannote': True,  # Try PyAnnote first, fallback to simple method
}

# Prosody and timing settings
PROSODY_SETTINGS = {
    'speed_range': (0.8, 1.2),     # Min and max speed multiplier
    'pitch_shift_range': (-2, 2),  # Semitones
    'preserve_timing': True,        # Stretch audio to match original duration
}

# API Keys (if using online translation)
# Set these as environment variables for security
GOOGLE_TRANSLATE_API_KEY = os.getenv('GOOGLE_TRANSLATE_API_KEY', '')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')
