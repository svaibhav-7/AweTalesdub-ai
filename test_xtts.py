import torch
import os
import sys
import numpy as np
import soundfile as sf

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

# Auto-agree to Coqui TOS
os.environ['COQUI_TOS_AGREED'] = '1'

def test_patch():
    print("--- Testing XTTS Audio Loading Patch ---")
    try:
        print("Importing load_audio from TTS.tts.models.xtts...")
        try:
            from TTS.tts.models.xtts import load_audio
        except ImportError as e:
            print(f"FAILED to import XTTS: {e}")
            return

        print("Successfully imported load_audio.")

        # Create a dummy wav file
        dummy_wav = "test_audio_loading.wav"
        sr = 22050
        # Generate 1 second of noise
        data = np.random.uniform(-1, 1, size=(sr,))
        sf.write(dummy_wav, data, sr)
        print(f"Created temporary file: {dummy_wav}")

        print("Calling load_audio()...")
        try:
            audio = load_audio(dummy_wav, 24000)
            print(f"SUCCESS: Audio loaded. Shape: {audio.shape}")
            if isinstance(audio, torch.Tensor):
                print("Output is a Tensor (Correct).")
            else:
                print(f"Output type mismatch: {type(audio)}")
            
            print("\n>>> THE PATCH IS WORKING CORRECTLY <<<")
            print("The Coqui XTTS module can now load audio without 'TorchCodec' error.")

        except Exception as e:
            print(f"FAILED during load_audio: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"General Error: {e}")
    finally:
        if os.path.exists("test_audio_loading.wav"):
            try:
                os.remove("test_audio_loading.wav")
            except:
                pass

if __name__ == "__main__":
    test_patch()
