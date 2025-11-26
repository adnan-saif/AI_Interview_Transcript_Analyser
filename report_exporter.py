import json
from datetime import datetime
import os
from fpdf import FPDF

def export_txt(results, file_path):
    """Export results to text file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("INTERVIEW ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("AUDIO METADATA:\n")
            f.write("-" * 20 + "\n")
            audio_meta = results.get('audio_metadata', {})
            f.write(f"Duration: {audio_meta.get('duration', 0):.2f} seconds\n")
     
            f.write("\nAI EVALUATION:\n")
            f.write("-" * 20 + "\n")
            evaluation = results.get('evaluation', 'No evaluation available')
            f.write(evaluation + "\n")
            
            f.write("SENTIMENT ANALYSIS:\n")
            f.write("-" * 20 + "\n")
            sentiment = results.get('sentiment', {})
            f.write(f"Overall Sentiment: {sentiment.get('label', 'N/A')}\n")
            f.write(f"Confidence Score: {sentiment.get('score', 0):.3f}\n\n")
            
            f.write("SKILLS & INFORMATION DETECTED:\n")
            f.write("-" * 20 + "\n")
            skills = results.get('skills_info', {})
            
            if skills.get('skills'):
                f.write(f"Technical Skills: {', '.join(skills['skills'])}\n")
            else:
                f.write("Technical Skills: None detected\n")
                
            if skills.get('languages'):
                f.write(f"Languages: {', '.join(skills['languages'])}\n")
            else:
                f.write("Languages: None detected\n")
                
            if skills.get('tools'):
                f.write(f"Tools: {', '.join(skills['tools'])}\n")
            else:
                f.write("Tools: None detected\n")
                
            if skills.get('degrees'):
                f.write(f"Education: {', '.join(skills['degrees'])}\n")
            else:
                f.write("Education: None detected\n")
                
            if skills.get('organizations'):
                f.write(f"Organizations: {', '.join(skills['organizations'])}\n")
            else:
                f.write("Organizations: None detected\n")
                
            if skills.get('projects'):
                f.write(f"Projects: {', '.join(skills['projects'])}\n")
            else:
                f.write("Projects: None detected\n")
                
            if skills.get('experience_durations'):
                durations = []
                for duration in skills['experience_durations']:
                    if isinstance(duration, dict):
                        durations.append(f"{duration.get('value', '')} {duration.get('unit', '')}")
                    else:
                        durations.append(str(duration))
                f.write(f"Experience Durations: {', '.join(durations)}\n")
            else:
                f.write("Experience Durations: None detected\n")
            
            f.write("DIARIZED TRANSCRIPT:\n")
            f.write("-" * 20 + "\n")
            segments = results.get('diarized_segments', [])
            for seg in segments:
                f.write(f"{seg.get('speaker', 'Unknown')} | {seg.get('start', 0):.2f}s - {seg.get('end', 0):.2f}s\n")
                f.write(f"{seg.get('text', '')}\n\n")
            
            f.write(f"\n\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"TXT report saved: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error saving TXT report: {str(e)}")
        return False

def export_json(results, file_path):
    """Export results to JSON file"""
    try:
        serializable_results = {}
        
        for key, value in results.items():
            if key == 'skills_info' and isinstance(value, dict):
                serializable_value = value.copy()
                if 'experience_durations' in serializable_value:
                    serializable_value['experience_durations'] = [
                        f"{d.get('value', '')} {d.get('unit', '')}" 
                        if isinstance(d, dict) else str(d)
                        for d in serializable_value['experience_durations']
                    ]
                serializable_results[key] = serializable_value
            else:
                serializable_results[key] = value
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        print(f"JSON report saved: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error saving JSON report: {str(e)}")
        return False

def export_pdf(results, file_path):
    """Simple PDF export using fpdf"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Interview Analysis Report", ln=1, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Audio Metadata", ln=1)
    pdf.set_font("Arial", size=10)
    audio_meta = results.get('audio_metadata', {})
    pdf.cell(200, 8, txt=f"Duration: {audio_meta.get('duration', 0):.2f} seconds", ln=1)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="AI Evaluation", ln=1)
    pdf.set_font("Arial", size=10)
    evaluation = results.get('evaluation', 'No evaluation available')
    pdf.multi_cell(0, 8, txt=evaluation)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Sentiment Analysis", ln=1)
    pdf.set_font("Arial", size=10)
    sentiment = results.get('sentiment', {})
    pdf.cell(200, 8, txt=f"Overall: {sentiment.get('label', 'N/A')} (Score: {sentiment.get('score', 0):.3f})", ln=1)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Skills Detected", ln=1)
    pdf.set_font("Arial", size=10)
    
    skills = results.get('skills_info', {})
    skills_text = ""
    if skills.get('skills'):
        skills_text += f"Technical: {', '.join(skills['skills'][:5])}\n"
    if skills.get('languages'):
        skills_text += f"Languages: {', '.join(skills['languages'])}\n"
    if skills.get('tools'):
        skills_text += f"Tools: {', '.join(skills['tools'])}\n"
    
    pdf.multi_cell(0, 8, txt=skills_text or "No skills detected")
    pdf.ln(5)
    
    # Diarized Transcript
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Diarized Transcript", ln=1)
    pdf.set_font("Arial", size=10)
    
    segments = results.get('diarized_segments', [])
    if segments:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(100, 8, txt="Speaker", ln=0)
        pdf.cell(50, 8, txt="Time", ln=0)
        pdf.cell(40, 8, txt="Text", ln=1)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        
        pdf.set_font("Arial", size=8)
        for i, segment in enumerate(segments[:20]):
            speaker = segment.get('speaker', 'Unknown')
            start = segment.get('start', 0)
            end = segment.get('end', 0)
            text = segment.get('text', '')[:80] + "..." if len(segment.get('text', '')) > 80 else segment.get('text', '')
            
            # Speaker
            pdf.cell(30, 6, txt=speaker, ln=0)
            pdf.cell(30, 6, txt=f"{start:.1f}s-{end:.1f}s", ln=0)
            pdf.multi_cell(130, 6, txt=text)
            pdf.ln(1)
            
            if pdf.get_y() > 250 and i < len(segments[:20]) - 1:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(100, 8, txt="Speaker", ln=0)
                pdf.cell(50, 8, txt="Time", ln=0)
                pdf.cell(40, 8, txt="Text", ln=1)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(2)
                pdf.set_font("Arial", size=8)
        
        if len(segments) > 20:
            pdf.ln(5)
            pdf.set_font("Arial", 'I', 8)
            pdf.cell(200, 6, txt=f"... and {len(segments) - 20} more segments", ln=1)
    else:
        pdf.multi_cell(0, 8, txt="No diarized transcript available")
    
    pdf.ln(5)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(200, 8, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
    
    pdf.output(file_path)
    print(f"PDF report saved: {file_path}")
    return True

def export_results(results, base_path):
    """Export results in all available formats"""
    base_dir = os.path.dirname(base_path)
    if base_dir and not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
    
    success_count = 0
    
    if export_txt(results, f"{base_path}.txt"):
        success_count += 1
    
    if export_json(results, f"{base_path}.json"):
        success_count += 1
    
    if export_pdf(results, f"{base_path}.pdf"):
        success_count += 1
    
    print(f"Successfully exported {success_count}/3 report files")
    return success_count > 0

def export_txt_only(results, base_path):
    """Export only TXT format"""
    file_path = f"{base_path}.txt"
    return export_txt(results, file_path)

def export_json_only(results, base_path):
    """Export only JSON format"""
    file_path = f"{base_path}.json"
    return export_json(results, file_path)

def export_pdf_only(results, base_path):
    """Export only PDF format"""
    file_path = f"{base_path}.pdf"
    return export_pdf(results, file_path)