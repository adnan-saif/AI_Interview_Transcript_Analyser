from audio_ingest import load_and_preprocess_audio
from transcribe_whisper import transcribe_audio_from_array
from diarize import diarize_whisper_segments_from_array, get_candidate_transcript, get_candidate_segments, determine_candidate_speaker
from clean_transcript import clean_transcript_segments, format_transcript_for_display
from sentiment import analyze_sentiment, analyze_segment_sentiments
from skills_extractor import extract_candidate_info
from summarize_and_decide import generate_evaluation

def run_full_pipeline(audio_path, candidate_speaker=None):
    """Run the complete interview analysis pipeline"""
    
    print("Starting Interview Analysis Pipeline...")
    
    # Audio ingestion
    print("Loading audio...")
    audio_array, sample_rate = load_and_preprocess_audio(audio_path)
    
    # Transcription
    print("Transcribing audio...")
    whisper_segments, full_transcript = transcribe_audio_from_array(audio_array, sample_rate)
    
    # Diarization
    print("Speaker diarization...")
    diarized_segments = diarize_whisper_segments_from_array(audio_array, sample_rate, whisper_segments)
    
    # Determine candidate speaker
    if candidate_speaker is None:
        print("Determining candidate speaker using AI...")
        candidate_speaker = determine_candidate_speaker(diarized_segments)
        print(f"Detected candidate speaker: {candidate_speaker}")
    
    # Transcript cleaning
    print("Cleaning transcript...")
    cleaned_segments = clean_transcript_segments(diarized_segments)
    
    # Get candidate transcript
    print("Extracting candidate speech...")
    candidate_segments = get_candidate_segments(cleaned_segments, candidate_speaker)
    candidate_transcript = get_candidate_transcript(cleaned_segments, candidate_speaker)
    
    # Sentiment analysis
    print("Analyzing sentiment...")
    sentiment = analyze_sentiment(candidate_transcript)
    segment_sentiments = analyze_segment_sentiments(cleaned_segments)
    
    # Skills extraction
    print("Extracting skills...")
    skills_info = extract_candidate_info(candidate_transcript)
    
    # AI Evaluation
    print("Generating AI evaluation...")
    formatted_transcript = format_transcript_for_display(cleaned_segments)
    evaluation = generate_evaluation(
        formatted_transcript,
        sentiment,
        skills_info,
        cleaned_segments
    )
    
    # Compile final results
    results = {
        'audio_metadata': {
            'duration': len(audio_array)/sample_rate,
            'sample_rate': sample_rate
        },
        'full_transcript': full_transcript,
        'diarized_segments': cleaned_segments,
        'candidate_segments': candidate_segments,
        'candidate_transcript': candidate_transcript,
        'sentiment': sentiment,
        'segment_sentiments': segment_sentiments,
        'skills_info': skills_info,
        'evaluation': evaluation,
        'candidate_speaker': candidate_speaker
    }
    
    print("Pipeline completed successfully!")
    return results

def export_results(results, base_path):
    """Export results in multiple formats"""
    from report_exporter import export_results as export_all
    success = export_all(results, base_path)
    if success:
        print(f"Reports exported successfully: {base_path}.[txt|json|pdf]")
    else:
        print("Some reports failed to export")
    return success