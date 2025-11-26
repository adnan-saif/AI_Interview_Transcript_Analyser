import whisper
import numpy as np
from config import WHISPER_MODEL_SIZE

# Load Whisper model once
whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)

def transcribe_audio_from_array(audio_array, sample_rate=16000):
    """Transcribe audio from numpy array - returns segments with timestamps"""
    print("Transcribing audio with Whisper from array...")
    
    audio_float = audio_array.astype(np.float32)
    result = whisper_model.transcribe(audio_float)
    
    print(f"Transcription complete. Segments: {len(result['segments'])}")
    return result["segments"], result["text"]

def transcribe_audio_from_file(audio_path):
    """Transcribe audio from file path - returns segments with timestamps"""
    print("Transcribing audio with Whisper from file...")
    
    result = whisper_model.transcribe(audio_path)
    
    print(f"Transcription complete. Segments: {len(result['segments'])}")
    return result["segments"], result["text"]