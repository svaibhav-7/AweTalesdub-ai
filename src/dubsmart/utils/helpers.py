import os
import json
import uuid
from typing import List, Dict, Any, Tuple

def ensure_dir(directory: str) -> str:
    """Ensure a directory exists."""
    os.makedirs(directory, exist_ok=True)
    return directory

def get_temp_filename(directory: str = 'temp', prefix: str = 'tmp_', suffix: str = '.wav') -> str:
    """Generate a unique temporary filename."""
    ensure_dir(directory)
    unique_id = str(uuid.uuid4())[:8]
    return os.path.join(directory, f"{prefix}{unique_id}{suffix}")

def save_json(data: Any, path: str) -> str:
    """Save data to a JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path

def load_json(path: str) -> Any:
    """Load data from a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def merge_overlapping_segments(segments: List[Dict[str, Any]], max_gap: float = 0.5) -> List[Dict[str, Any]]:
    """Merge consecutive segments if they belong to the same speaker and are close in time."""
    if not segments:
        return []
    
    merged = [segments[0].copy()]
    for seg in segments[1:]:
        last = merged[-1]
        if (seg['speaker'] == last['speaker'] and 
            seg['start'] - last['end'] <= max_gap):
            last['end'] = seg['end']
            if 'text' in seg and 'text' in last:
                last['text'] += " " + seg['text']
        else:
            merged.append(seg.copy())
    return merged
