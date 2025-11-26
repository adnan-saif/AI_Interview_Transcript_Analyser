import numpy as np
import librosa
from resemblyzer import VoiceEncoder, preprocess_wav
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from config import WHISPER_MODEL_SIZE
import google.generativeai as genai
from config import GEMINI_MODEL

model = genai.GenerativeModel(GEMINI_MODEL)

# Load models
encoder = VoiceEncoder()

def get_segment_embedding_from_array(audio_array, sample_rate, start, end):
    """Get embedding from audio array segment"""
    segment = audio_array[int(start * sample_rate):int(end * sample_rate)]
    segment = preprocess_wav(segment)
    embed = encoder.embed_utterance(segment)
    return embed

def detect_num_speakers(embeddings, max_speakers=4):
    """Your existing speaker detection"""
    best_score = -1
    best_k = 1

    for k in range(2, max_speakers + 1):
        clustering = AgglomerativeClustering(n_clusters=k).fit(embeddings)
        score = silhouette_score(embeddings, clustering.labels_)
        if score > best_score:
            best_score = score
            best_k = k
    return best_k

def diarize_whisper_segments_from_array(audio_array, sample_rate, whisper_segments, max_speakers=4):
    """Diarization using audio array instead of file path"""
    embeddings = []
    
    print("Generating speaker embeddings from audio array...")
    for seg in whisper_segments:
        emb = get_segment_embedding_from_array(audio_array, sample_rate, seg["start"], seg["end"])
        embeddings.append(emb)

    if not embeddings:
        return []

    embeddings = np.vstack(embeddings)

    num_speakers = detect_num_speakers(embeddings, max_speakers)
    print(f"Detected speakers: {num_speakers}")

    clustering = AgglomerativeClustering(n_clusters=num_speakers)
    labels = clustering.fit_predict(embeddings)

    diarized = []
    for seg, spk in zip(whisper_segments, labels):
        diarized.append({
            "speaker": f"Speaker_{spk+1}",
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"]
        })

    return diarized

def determine_candidate_speaker(diarized_segments):
    """Use Gemini to determine which speaker is the candidate/interviewee"""
    try:
        conversation_text = ""
        for segment in diarized_segments[:10]:
            conversation_text += f"{segment['speaker']}: {segment['text']}\n"
        
        prompt = f"""
        Analyze this interview conversation and identify which speaker is the candidate/interviewee (the person being interviewed).
        
        Conversation:
        {conversation_text}
        
        Based on the content, which speaker is most likely the candidate being interviewed? 
        Return ONLY the speaker name exactly as it appears in the conversation (e.g., "Speaker_1" or "Speaker_2").
        Do not add any explanation, only the speaker name as mention in conversation.
        """
        
        response = model.generate_content(prompt)
        candidate_speaker = response.text.strip()
        
        return candidate_speaker
    
    except Exception:
        return "Speaker_1"

def get_candidate_segments(diarized_segments, candidate_speaker="Speaker_1"):
    """Extract only candidate segments"""
    return [seg for seg in diarized_segments if seg.get("speaker") == candidate_speaker]

def get_candidate_transcript(diarized_segments, candidate_speaker="Speaker_1"):
    """Get candidate's full transcript"""
    candidate_segments = get_candidate_segments(diarized_segments, candidate_speaker)
    return " ".join([seg.get("text", "") for seg in candidate_segments])