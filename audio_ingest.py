import librosa
import numpy as np
import soundfile as sf
import tempfile

def validate_audio(file_path):
    """Validate audio file"""
    allowed_extensions = ['.mp3', '.wav', '.m4a', '.flac']
    if not any(file_path.lower().endswith(ext) for ext in allowed_extensions):
        raise ValueError(f"Unsupported file format. Allowed: {allowed_extensions}")
    return True

def load_and_preprocess_audio(file_path):
    """Load and preprocess audio using librosa only"""
    print("Loading and preprocessing audio...")
    
    validate_audio(file_path)
    audio, sr = librosa.load(file_path, sr=16000, mono=True)
    audio = librosa.util.normalize(audio)
    print(f"Audio loaded: {len(audio)/sr:.2f} seconds, Sample rate: {sr}")
    
    return audio, sr

def save_audio_to_temp(audio, sr):
    """Save audio to temporary file for Whisper"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    sf.write(temp_file.name, audio, sr)
    return temp_file.name