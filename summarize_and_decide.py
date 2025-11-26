import google.generativeai as genai
from config import GEMINI_MODEL

model = genai.GenerativeModel(GEMINI_MODEL)

def build_evaluation_prompt(transcript, sentiment, skills_info, diarized_segments):
    """Build comprehensive prompt for Gemini evaluation"""  
    prompt = f"""
You are an HR interview evaluation assistant.

INTERVIEW TRANSCRIPT:
{transcript}

SENTIMENT ANALYSIS: {sentiment['label']} (confidence: {sentiment['score']:.2f})

SKILLS DETECTED:
- Technical Skills: {', '.join(skills_info['skills']) if skills_info['skills'] else 'None'}
- Languages: {', '.join(skills_info['languages']) if skills_info['languages'] else 'None'}
- Tools: {', '.join(skills_info['tools']) if skills_info['tools'] else 'None'}
- Education: {', '.join(skills_info['degrees']) if skills_info['degrees'] else 'None'}
- Organizations: {', '.join(skills_info['organizations']) if skills_info['organizations'] else 'None'}
- Experience: {skills_info['experience_durations'] if skills_info['experience_durations'] else 'None'}

YOUR TASKS:
1. Generate a concise summary of the interview (4-5 lines)
2. Provide a clear HIRE or NO-HIRE recommendation
3. Provide confidence score (0-100)
4. Divide interview into 3 logical sections and evaluate candidate performance in each
5. Mention key points discussed in each section
6. Provide reasoning for your recommendation

OUTPUT FORMAT:
Summary: [4-5 line summary]

Recommendation: [HIRE/NO-HIRE]

Confidence: [0-100]

Section 1: [Section name]
- Performance: [Evaluation in couple of sentences]
- Key Points: [Key discussion points]

Section 2: [Section name]  
- Performance: [Evaluation in couple of sentences]
- Key Points: [Key discussion points]

Section 3: [Section name]
- Performance: [Evaluation in couple of sentences]
- Key Points: [Key discussion points]

Reasoning: [Detailed reasoning for recommendation]

Do not use markdown or bold formatting, provide proper spacing for paragraph and lines.
"""
    return prompt

def generate_evaluation(transcript, sentiment, skills_info, diarized_segments):
    """Generate final evaluation using Gemini"""
    prompt = build_evaluation_prompt(transcript, sentiment, skills_info, diarized_segments)
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating evaluation: {str(e)}"