"""
Example usage of the Audio Dubbing System
"""
from audio_dubbing import AudioDubber
import config

def example_basic_usage():
    """Basic example: Dub an audio file"""
    
    print("Example 1: Basic Audio Dubbing")
    print("-" * 50)
    
    # Create dubber instance
    dubber = AudioDubber()
    
    # Dub audio from English to Hindi
    results = dubber.dub_audio(
        input_file="sample_audio.wav",  # Your input audio
        target_language="hi",            # Hindi
        output_file="output/dubbed_hindi.wav"
    )
    
    if results['status'] == 'success':
        print(f"✓ Success!")
        print(f"  Detected: {results['detected_language_name']}")
        print(f"  Speakers: {results['num_speakers']}")
        print(f"  Output: {results['output_file']}")
    else:
        print(f"✗ Failed: {results.get('error')}")


def example_with_options():
    """Example with advanced options"""
    
    print("\nExample 2: Advanced Options")
    print("-" * 50)
    
    dubber = AudioDubber(use_pyannote=False)  # Use simple diarization
    
    # Dub with background preservation
    results = dubber.dub_audio(
        input_file="interview.wav",
        target_language="te",  # Telugu
        output_file="output/interview_telugu.wav",
        preserve_background=True,  # Keep background sounds
        save_intermediates=True    # Save intermediate files for debugging
    )
    
    print(f"Status: {results['status']}")
    print(f"Segments processed: {results.get('num_segments', 0)}")


def example_multiple_languages():
    """Example: Dub same audio to multiple languages"""
    
    print("\nExample 3: Multiple Target Languages")
    print("-" * 50)
    
    dubber = AudioDubber()
    input_audio = "podcast.wav"
    
    for target_lang in ['en', 'hi', 'te']:
        print(f"\nDubbing to {config.SUPPORTED_LANGUAGES[target_lang]}...")
        
        results = dubber.dub_audio(
            input_file=input_audio,
            target_language=target_lang,
            output_file=f"output/podcast_{target_lang}.wav",
            save_intermediates=False  # Don't save intermediates
        )
        
        if results['status'] == 'success':
            print(f"  ✓ {target_lang}: {results['output_file']}")
        else:
            print(f"  ✗ {target_lang}: {results.get('error')}")


def example_step_by_step():
    """Example: Run pipeline step-by-step with custom processing"""
    
    print("\nExample 4: Step-by-Step Processing")
    print("-" * 50)
    
    from audio_processor import process_audio_pipeline
    from speaker_diarization import diarize_audio_file
    from transcription import transcribe_with_speaker_diarization
    from translation import Translator
    from voice_synthesis import VoiceSynthesizer
    from audio_mixer import mix_dubbed_audio
    
    input_file = "sample.wav"
    target_lang = "hi"
    
    # Step 1: Preprocess audio
    print("1. Preprocessing audio...")
    clean_audio, vad_segments = process_audio_pipeline(input_file)
    print(f"   ✓ Clean audio: {clean_audio}")
    
    # Step 2: Speaker diarization
    print("2. Identifying speakers...")
    speaker_segments = diarize_audio_file(clean_audio)
    print(f"   ✓ Found {len(set(s['speaker'] for s in speaker_segments))} speakers")
    
    # Step 3: Transcription
    print("3. Transcribing...")
    detected_lang, transcribed = transcribe_with_speaker_diarization(
        clean_audio, speaker_segments
    )
    print(f"   ✓ Detected language: {detected_lang}")
    
    # Step 4: Translation
    print("4. Translating...")
    translator = Translator()
    translated = translator.translate_segments(transcribed, detected_lang, target_lang)
    print(f"   ✓ Translated {len(translated)} segments")
    
    # Step 5: Voice synthesis
    print("5. Synthesizing voices...")
    synthesizer = VoiceSynthesizer()
    synthesized = synthesizer.synthesize_all_segments(
        translated, target_lang, "temp/tts"
    )
    print(f"   ✓ Generated {len(synthesized)} audio segments")
    
    # Step 6: Mix audio
    print("6. Mixing final audio...")
    output = mix_dubbed_audio(synthesized, "output/step_by_step.wav")
    print(f"   ✓ Final output: {output}")


if __name__ == "__main__":
    print("=" * 50)
    print("AUDIO DUBBING SYSTEM - EXAMPLES")
    print("=" * 50)
    
    # Run examples (comment out the ones you don't want to run)
    
    # Example 1: Basic usage
    # example_basic_usage()
    
    # Example 2: Advanced options
    # example_with_options()
    
    # Example 3: Multiple languages
    # example_multiple_languages()
    
    # Example 4: Step-by-step
    # example_step_by_step()
    
    print("\n" + "=" * 50)
    print("To run an example, uncomment it in the __main__ section")
    print("=" * 50)
