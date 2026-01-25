from setuptools import setup, find_packages

setup(
    name="dubsmart",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "openai-whisper",
        "torch",
        "torchaudio",
        "transformers",
        "TTS",
        "pydub",
        "librosa",
        "soundfile",
        "pyannote.audio",
    ],
    entry_points={
        "console_scripts": [
            "dubsmart=dubsmart.main:main",
        ],
    },
)
