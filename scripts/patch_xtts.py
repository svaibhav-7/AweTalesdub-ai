
import os
import sys
import shutil

def patch_xtts():
    """
    Patches the XTTS model file in the installed TTS library to fallback to librosa/soundfile
    instead of failing with TorchCodec errors.
    """
    try:
        import TTS.tts.models.xtts as xtts_module
        xtts_path = xtts_module.__file__
        print(f"Found XTTS model file at: {xtts_path}")
        
        with open(xtts_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already patched
        if "falling back to librosa" in content:
            print("XTTS is already patched.")
            return

        print("Applying patch...")
        
        # Original code block to replace
        original_code = """    # torchaudio should chose proper backend to load audio depending on platform
    audio, lsr = torchaudio.load(audiopath)"""
    
        # New code block
        new_code = """    # torchaudio should chose proper backend to load audio depending on platform
    try:
        audio, lsr = torchaudio.load(audiopath)
    except Exception as e:
        print(f" > torchaudio load failed ({e}), falling back to librosa.")
        import librosa
        audio, lsr = librosa.load(audiopath, sr=None)
        audio = torch.from_numpy(audio).float()
        if len(audio.shape) == 1:
            audio = audio.unsqueeze(0)"""
            
        if original_code in content:
            new_content = content.replace(original_code, new_code)
            
            # Backup original
            shutil.copy2(xtts_path, xtts_path + ".bak")
            
            with open(xtts_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print("Successfully patched XTTS audio loading!")
        else:
            print("Could not find the exact code block to patch. It might be different version or already modified.")
            
    except ImportError:
        print("TTS library not found. Please install requirements first.")
    except Exception as e:
        print(f"Error patching XTTS: {e}")

if __name__ == "__main__":
    patch_xtts()
