import spacy
from sentence_transformers import SentenceTransformer, util
import re
import nltk
from nltk import ngrams
from config import SPACY_MODEL, EMBEDDING_MODEL, MASTER_SKILLS, TECH_SKILLS, LANGUAGE_SKILLS, TOOLS, DEGREES

# Download required NLTK data
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

# Load models
nlp = spacy.load(SPACY_MODEL)
emb_model = SentenceTransformer(EMBEDDING_MODEL)

# Precompute skill embeddings
skill_embeddings = emb_model.encode(MASTER_SKILLS, convert_to_tensor=True)

def extract_duration(text):
    """Your existing duration extraction"""
    pattern = r"(\d+)\s*(year|years|month|months)"
    matches = re.findall(pattern, text.lower())
    durations = [{"value": m[0], "unit": m[1]} for m in matches]
    return durations

def extract_candidate_info(text):
    """Your existing skills extraction function"""
    doc = nlp(text)

    extracted = {
        "skills": set(),
        "languages": set(),
        "tools": set(),
        "degrees": set(),
        "organizations": set(),
        "projects": set(),
        "experience_durations": [],
    }

    # NER Extraction
    for ent in doc.ents:
        if ent.label_ == "ORG":
            extracted["organizations"].add(ent.text)
        if ent.label_ in ["WORK_OF_ART", "PRODUCT"]:
            extracted["projects"].add(ent.text)
        if ent.label_ == "EDUCATION":
            extracted["degrees"].add(ent.text)

    # Duration Extraction
    extracted["experience_durations"] = extract_duration(text)

    # Phrase-level embedding matching
    sentences = nltk.sent_tokenize(text)
    all_phrases = set()

    for sent in sentences:
        words = sent.split()
        for n in [1, 2, 3]:
            for gram in ngrams(words, n):
                phrase = " ".join(gram)
                all_phrases.add(phrase)

    phrase_list = list(all_phrases)
    if phrase_list:
        phrase_embeddings = emb_model.encode(phrase_list, convert_to_tensor=True)
        sim = util.cos_sim(phrase_embeddings, skill_embeddings)

        for i, phrase in enumerate(phrase_list):
            score = float(sim[i].max())
            idx = int(sim[i].argmax())

            if score > 0.60:
                extracted["skills"].add(MASTER_SKILLS[idx])

    # Language extraction
    for lang in LANGUAGE_SKILLS:
        if lang.lower() in text.lower():
            extracted["languages"].add(lang)

    # Degree extraction
    for deg in DEGREES:
        if deg.lower() in text.lower():
            extracted["degrees"].add(deg)

    # Convert sets to lists for JSON serialization
    for key in extracted:
        if isinstance(extracted[key], set):
            extracted[key] = list(extracted[key])
            
    return extracted

def format_experience_durations(durations):
    """Format experience durations for display"""
    formatted = []
    for duration in durations:
        if isinstance(duration, dict):
            formatted.append(f"{duration.get('value', '')} {duration.get('unit', '')}")
        else:
            formatted.append(str(duration))
    return formatted