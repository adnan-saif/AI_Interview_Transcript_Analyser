from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from config import SENTIMENT_MODEL

# Load model once
sent_model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL)
tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)

def analyze_sentiment(text):
    """Your existing sentiment analysis function"""
    text = text.replace("\n", " ")
    
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding="max_length",
    )
    
    inputs.pop("token_type_ids", None)
    
    with torch.no_grad():
        outputs = sent_model(**inputs)
    
    scores = torch.softmax(outputs.logits, dim=1)[0].tolist()
    labels = ["negative", "neutral", "positive"]
    
    max_score = max(scores)
    max_index = scores.index(max_score)
    
    return {
        "label": labels[max_index],
        "score": max_score,
        "scores": {
            "negative": scores[0],
            "neutral": scores[1], 
            "positive": scores[2]
        }
    }

def analyze_segment_sentiments(segments):
    """Analyze sentiment for each segment"""
    segment_sentiments = []
    for segment in segments:
        sentiment = analyze_sentiment(segment['text'])
        segment_sentiments.append({
            **segment,
            "sentiment": sentiment
        })
    return segment_sentiments