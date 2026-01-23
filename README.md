# Multilingual Audio Dubbing System
An AI-powered audio dubbing pipeline that automatically detects source language, identifies different speakers, translates speech, and generates dubbed audio with separate voices per speaker.

## 🎯 Features

✅ **Auto-detects source language** (English / Hindi / Telugu)  
✅ **Rejects same-language dubbing** (source ≠ target validation)  
✅ **Auto-assigns speaker IDs** (speaker diarization)  
✅ **Assigns separate voices per speaker**  
✅ **Translates to target language**  
✅ **Includes noise suppression**  
✅ **Preserves timing and emotion**  
✅ **Hackathon-realistic** (no training required, uses pre-trained models)

## 📋 Prerequisites

### System Requirements

- **Python 3.8+**
- **FFmpeg** (must be installed system-wide)

#### Install FFmpeg

**Windows:**
```powershell
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### Python Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

**Note:** The first time you run Whisper, it will download model files (~1-3 GB depending on model size).

## 🚀 Quick Start

### Basic Usage

```bash
python audio_dubbing.py input.wav hi output.wav
```

This will:
1. Detect the language in `input.wav`
2. Translate it to Hindi (`hi`)
3. Generate dubbed audio as `output.wav`

### Command-Line Options

```bash
python audio_dubbing.py <input> <target_lang> <output> [options]

Arguments:
  input             Input audio file (WAV, MP3, etc.)
  target_lang       Target language: en (English), hi (Hindi), te (Telugu)
  output            Output audio file

Options:
  --use-pyannote           Use PyAnnote for better speaker diarization
                          (requires HuggingFace token)
  --preserve-background    Preserve background sounds from original
  --no-intermediates       Don't save intermediate processing files
```

### Examples

**English to Hindi:**
```bash
python audio_dubbing.py interview.wav hi interview_hindi.wav
```

**Telugu to English:**
```bash
python audio_dubbing.py podcast_telugu.wav en podcast_english.wav
```

**With background preservation:**
```bash
python audio_dubbing.py video_audio.wav te dubbed_telugu.wav --preserve-background
```

## 💻 Python API Usage

```python
from audio_dubbing import AudioDubber

# Create dubber instance
dubber = AudioDubber()

# Dub audio
results = dubber.dub_audio(
    input_file="sample.wav",
    target_language="hi",  # Hindi
    output_file="output.wav"
)

if results['status'] == 'success':
    print(f"Dubbed successfully: {results['output_file']}")
    print(f"Detected language: {results['detected_language_name']}")
    print(f"Number of speakers: {results['num_speakers']}")
```

See [`example_usage.py`](example_usage.py) for more examples.

## 🔁 How It Works - Complete Pipeline

```
Input Audio
    ↓
Audio Extraction & Conversion (mono, 16kHz)
    ↓
Noise Suppression (FFmpeg afftdn filter)
    ↓
Voice Activity Detection (Silero VAD)
    ↓
Speaker Diarization (PyAnnote or energy-based fallback)
    ↓
Speech-to-Text (Whisper - multilingual)
    ↓
Automatic Language Detection (Whisper)
    ↓
Source ≠ Target Validation
    ↓
Text Segmentation & Alignment (merge speaker segments)
    ↓
Translation (MarianMT - source → target)
    ↓
Voice Assignment (unique voice per speaker)
    ↓
Emotion-aware Text-to-Speech (gTTS with prosody)
    ↓
Timing Alignment (match original duration)
    ↓
Audio Mixing (combine all segments)
    ↓
Final Dubbed Audio
```

## 🧩 Project Structure

```
dubsmart-ai/
├── audio_dubbing.py          # Main pipeline orchestrator
├── audio_processor.py         # Audio preprocessing (noise, VAD)
├── speaker_diarization.py     # Speaker identification
├── transcription.py           # Speech-to-text (Whisper)
├── translation.py             # Translation (MarianMT)
├── voice_synthesis.py         # Text-to-speech (gTTS)
├── audio_mixer.py             # Audio mixing
├── config.py                  # Configuration settings
├── utils.py                   # Utility functions
├── example_usage.py           # Usage examples
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── temp/                      # Temporary processing files
├── output/                    # Output directory
└── models/                    # Downloaded models cache
```

## ⚙️ Configuration

Edit [`config.py`](config.py) to customize:

- **Whisper Model**: Change `WHISPER_MODEL` (options: `tiny`, `base`, `small`, `medium`, `large`)
- **Translation Method**: Change `TRANSLATION_METHOD` (`marian`, `google`, `gemini`)
- **TTS Engine**: Change `TTS_ENGINE` (`gtts`, `pyttsx3`, `coqui`)
- **Voice Mappings**: Customize voices per speaker per language
- **Audio Settings**: Sample rate, noise reduction parameters, etc.

### Using PyAnnote (Better Speaker Diarization)

PyAnnote provides better speaker diarization but requires a HuggingFace token:

1. Get a token from [HuggingFace](https://huggingface.co/settings/tokens)
2. Accept the [PyAnnote model terms](https://huggingface.co/pyannote/speaker-diarization)
3. Set environment variable:
   ```bash
   # Windows PowerShell
   $env:HUGGINGFACE_TOKEN="your_token_here"
   
   # Linux/Mac
   export HUGGINGFACE_TOKEN="your_token_here"
   ```
4. Run with `--use-pyannote` flag

## 🎤 Supported Languages

| Code | Language |
|------|----------|
| `en` | English  |
| `hi` | Hindi    |
| `te` | Telugu   |

> **Note:** You can extend language support by modifying `config.py` and ensuring the translation models support your language pairs.

## 🔧 Troubleshooting

### "FFmpeg not found"
- Install FFmpeg system-wide (see Prerequisites section)
- Ensure it's in your PATH

### "Model download failed"
- Check internet connection (Whisper downloads ~1-3GB on first run)
- Models are cached in `~/.cache/whisper/`

### "PyAnnote authentication failed"
- Set `HUGGINGFACE_TOKEN` environment variable
- Accept model terms at https://huggingface.co/pyannote/speaker-diarization

### "Translation quality is poor"
- MarianMT has limited support for some Indic language pairs
- Consider using Google Translate API (requires API key in `config.py`)

### "Speaker diarization not working well"
- Try with `--use-pyannote` for better quality
- Or use audio with clearly distinct speakers
- Simple fallback works best with 1-2 speakers

## 📊 Performance Tips

1. **Use smaller Whisper models** for faster processing: `WHISPER_MODEL = 'tiny'` or `'base'`
2. **Disable intermediate file saving** with `--no-intermediates`
3. **Use GPU** if available (automatically detected for Whisper and PyAnnote)
4. **Process shorter clips** (1-2 minutes recommended for demos)

## 🎓 Hackathon Demo Tips

1. **Prepare 2-3 sample audio files** with different scenarios:
   - Single speaker (news anchor)
   - Two speakers (interview/conversation)
   - With background music/noise

2. **Show intermediate outputs**:
   - `temp/speaker_segments.json` - Speaker diarization results
   - `temp/transcription.json` - Original transcription
   - `temp/translated_segments.json` - Translated text

3. **Highlight key features**:
   - Language auto-detection
   - Same-language rejection
   - Multiple speakers with different voices
   - Timing preservation

4. **Be ready to explain each step** using the pipeline diagram

## 📝 License

This project is for educational and hackathon purposes.

## 🙏 Acknowledgments

- **OpenAI Whisper** - Multilingual speech recognition
- **PyAnnote** - Speaker diarization
- **MarianMT** - Neural machine translation
- **gTTS** - Text-to-speech synthesis
- **FFmpeg** - Audio processing

---

**Made for hackathons | No training required | Uses only pre-trained models**
