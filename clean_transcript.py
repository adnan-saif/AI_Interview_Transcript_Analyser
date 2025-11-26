import re
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt', quiet=True)

def clean_text(text):
    """Clean transcript text - remove fillers, normalize punctuation"""
    fillers = [
    "uh", "um", "uhh", "umm",
    "ah", "er", "eh", "hmm",
    "kinda", "sorta",
    "oh", "ohhhh",
    "huh", "mm-hmm", "mmhm", 
    "lmao", "lol"
    ]

    for filler in fillers:
        text = re.sub(r'\b' + filler + r'\b', '', text, flags=re.IGNORECASE)
    
    text = re.sub(r'\s+', ' ', text)
    
    text = re.sub(r'\s+([.,!?;])', r'\1', text)
    text = re.sub(r'([.,!?;])(\w)', r'\1 \2', text)
    
    return text.strip()

def clean_transcript_segments(segments):
    """Clean all transcript segments"""
    cleaned_segments = []
    for segment in segments:
        cleaned_text = clean_text(segment.get('text', ''))
        if cleaned_text: 
            cleaned_segments.append({
                **segment,
                'text': cleaned_text
            })
    return cleaned_segments

def format_transcript_for_display(segments):
    """Format transcript for nice display"""
    formatted = []
    for seg in segments:
        formatted.append(f"{seg['speaker']} | {seg['start']:.2f}s → {seg['end']:.2f}s\n{seg['text']}\n")
    return "\n".join(formatted)