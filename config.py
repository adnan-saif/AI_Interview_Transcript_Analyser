import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key = API_KEY)

# Model Configuration
WHISPER_MODEL_SIZE = "small"
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
SPACY_MODEL = "en_core_web_lg"
GEMINI_MODEL = "gemini-2.0-flash"

# Skills Ontology
TECH_SKILLS = [
    "Advertising", "Sales", "Customer Service", "Marketing", 
    "Website Development", "Content Creation", "Data Entry", 
    "Communication", "Management", "Team Management", "Project Management"
]

LANGUAGE_SKILLS = ["Italian", "Spanish", "English"]
TOOLS = ["Microsoft Word", "Microsoft Excel", "PowerPoint", "Google Docs", "Google Sheets"]
DEGREES = ["Bachelor", "University Degree", "Computer Science", "Engineering"]

MASTER_SKILLS = TECH_SKILLS + LANGUAGE_SKILLS + TOOLS + DEGREES

# Audio Processing
SAMPLE_RATE = 16000
MAX_AUDIO_DURATION = 3600