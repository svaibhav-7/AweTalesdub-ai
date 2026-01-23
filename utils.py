"""
Utility functions for the Audio Dubbing System
"""
import json
import logging
import os
from typing import List, Dict, Any
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name"""
    return logging.getLogger(name)

def save_segments_json(segments: List[Dict[str, Any]], output_path: str) -> None:
    """
    Save segments to a JSON file
    
    Args:
        segments: List of segment dictionaries
        output_path: Path to save the JSON file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)
    get_logger(__name__).info(f"Saved segments to {output_path}")

def load_segments_json(input_path: str) -> List[Dict[str, Any]]:
    """
    Load segments from a JSON file
    
    Args:
        input_path: Path to the JSON file
        
    Returns:
        List of segment dictionaries
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        segments = json.load(f)
    get_logger(__name__).info(f"Loaded {len(segments)} segments from {input_path}")
    return segments

def format_timestamp(seconds: float) -> str:
    """
    Format seconds as HH:MM:SS.mmm
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"

def ensure_dir(directory: str) -> None:
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        directory: Path to directory
    """
    os.makedirs(directory, exist_ok=True)

def get_temp_filename(prefix: str, extension: str) -> str:
    """
    Generate a temporary filename with timestamp
    
    Args:
        prefix: Prefix for the filename
        extension: File extension (without dot)
        
    Returns:
        Temporary filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}_{timestamp}.{extension}"

def validate_language(lang_code: str, supported_languages: Dict[str, str]) -> bool:
    """
    Validate if a language code is supported
    
    Args:
        lang_code: Language code to validate
        supported_languages: Dictionary of supported language codes
        
    Returns:
        True if language is supported, False otherwise
    """
    return lang_code in supported_languages

def merge_overlapping_segments(segments: List[Dict[str, Any]], 
                               tolerance: float = 0.1) -> List[Dict[str, Any]]:
    """
    Merge segments that are very close or overlapping
    
    Args:
        segments: List of segment dictionaries with 'start' and 'end' keys
        tolerance: Maximum gap between segments to merge (seconds)
        
    Returns:
        List of merged segments
    """
    if not segments:
        return []
    
    # Sort by start time
    sorted_segments = sorted(segments, key=lambda x: x['start'])
    merged = [sorted_segments[0].copy()]
    
    for current in sorted_segments[1:]:
        last = merged[-1]
        
        # Check if segments should be merged
        if current['start'] - last['end'] <= tolerance:
            # Merge segments
            last['end'] = max(last['end'], current['end'])
            # Combine text if present
            if 'text' in last and 'text' in current:
                last['text'] += ' ' + current['text']
        else:
            merged.append(current.copy())
    
    return merged

def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences (simple implementation)
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
    """
    import re
    # Simple sentence splitting
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def estimate_speech_duration(text: str, words_per_minute: int = 150) -> float:
    """
    Estimate how long it takes to speak given text
    
    Args:
        text: Input text
        words_per_minute: Average speaking rate
        
    Returns:
        Estimated duration in seconds
    """
    words = len(text.split())
    minutes = words / words_per_minute
    return minutes * 60

def print_progress_bar(iteration: int, total: int, prefix: str = '', 
                       suffix: str = '', length: int = 50, fill: str = '█'):
    """
    Print a progress bar to console
    
    Args:
        iteration: Current iteration
        total: Total iterations
        prefix: Prefix string
        suffix: Suffix string
        length: Character length of bar
        fill: Bar fill character
    """
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')
    if iteration == total:
        print()
