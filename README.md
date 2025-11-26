# 🎤 AI Interview Transcript Analyzer

## 📘 Introduction
The **AI Interview Transcript Analyzer** is an intelligent, end-to-end AI system that transforms raw interview audio into structured transcripts, speaker-separated dialogue, sentiment insights, skill detection, and a final HR-style evaluation.  
Powered by **Whisper**, **Resemblyzer**, **SpaCy**, **Sentence Transformers**, and **Google Gemini**, the system automates key HR processes with high accuracy and professional output formatting.

---

## 🎯 Objectives
- Generate **high-quality transcriptions** using Whisper.
- Detect and separate speakers through **AI diarization**.
- Clean transcripts for readability and structure.
- Extract **skills**, experience, tools, and languages using NLP.
- Analyze **sentiment tone** of the candidate.
- Generate a full **summary + recommendation** using Google Gemini 2.0 Flash.
- Provide a **Streamlit-based UI** for interaction and report downloads.

---

## 🧰 Technologies Used

- **Programming Language**: Python  
- **AI Models**:
  - Whisper (Transcription)
  - Resemblyzer (Speaker Embeddings)
  - SpaCy (NER)
  - SentenceTransformer (Skill Similarity)
  - RoBERTa (Sentiment Analysis)
  - Google Gemini 2.0 Flash (HR Evaluation)
- **Libraries/Frameworks**:
  - librosa
  - soundfile
  - scikit-learn
  - transformers
  - streamlit
  - reportlab
- **Tools/Platforms**: VS Code, Streamlit Cloud

---

## 🧠 Workflow Overview

| Step | Module | Description |
|------|---------|-------------|
| 1️⃣ | **Audio Ingestion** | Validate, load, normalize interview audio |
| 2️⃣ | **Whisper Transcription** | Generate text + timestamps |
| 3️⃣ | **Diarization** | Identify candidate/interviewer via clustering + Gemini |
| 4️⃣ | **Cleaning** | Remove fillers, normalize punctuation |
| 5️⃣ | **Sentiment Analysis** | Analyze emotional tone of the candidate |
| 6️⃣ | **Skill Extraction** | Detect technical, language, tool & education skills |
| 7️⃣ | **Gemini Evaluation** | Generate summary, sections & hire/no-hire |
| 8️⃣ | **Streamlit UI** | Display insights & allow report downloads |

---

## 💻 Application Features

### 📝 Accurate Transcription
- Whisper generates **high-quality speech-to-text** with timestamps.

### 🗣️ Smart Speaker Diarization
- Resemblyzer clustering determines speakers.
- Gemini identifies **who is the candidate**.

### 🧹 Transcript Cleaning
- Removes filler words (uh, um, ah).  
- Fixes spacing, punctuation, and readability.

### 😊 Sentiment Analysis
- RoBERTa model analyzes candidate’s emotional tone.

### 🧠 Skill Extraction
- Detects:
  - Technical skills  
  - Tools  
  - Languages  
  - Education  
  - Organizations  
  - Experience durations  

### 🤖 AI HR Evaluation (via Gemini)
- Generates:
  - 4–5 line summary  
  - 3-section performance analysis  
  - Hire/No-Hire decision  
  - Confidence score  
  - Detailed reasoning  

### 📊 Interactive Streamlit UI
- Dashboard with metrics  
- Skills tab  
- Transcript tab  
- AI evaluation tab  
- PDF, JSON, and TXT export  

---

## 🧭 How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/adnan-saif/AI-Interview-Analyzer.git
cd AI-Interview-Analyzer
