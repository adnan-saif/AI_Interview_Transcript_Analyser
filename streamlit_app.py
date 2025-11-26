import streamlit as st
import tempfile
import os
from datetime import datetime
from pipeline import run_full_pipeline
from report_exporter import export_txt, export_json, export_pdf
import json
import base64

# Page configuration
st.set_page_config(
    page_title="AI Interview Transcript Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
def load_css():
    with open("2/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(image_file):
    bin_str = get_base64_of_bin_file(image_file)
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    # Load custom CSS
    load_css()

    st.markdown("""
    <div class="main-header fade-in">
        <h1 style="margin:0; font-size: 3rem; font-weight: 700;">AI Interview Transcript Analyzer</h1>
        <p style="margin:0; font-size: 1.2rem; opacity: 0.9;">Professional Interview Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None

    # File upload section
    st.markdown("""
    <div class="upload-area fade-in">
        <h3 style="color: #667eea; margin-bottom: 1rem;">Upload Interview Audio</h3>
        <p style="color: #666; margin-bottom: 2rem;">Supported formats: MP3, WAV, M4A</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an audio file", 
        type=['mp3', 'wav', 'm4a'],
        help="Upload your interview recording for analysis",
        label_visibility="collapsed"
    )
    
    # Store uploaded file in session state
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.success(f"File ready: {uploaded_file.name}")
    
    st.markdown(" ")

    if st.session_state.uploaded_file is not None and not st.session_state.analysis_complete:
        if st.button("Start AI Analysis", type="primary", use_container_width=True):

            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(st.session_state.uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(st.session_state.uploaded_file.getvalue())
                audio_path = tmp_file.name
            
            try:
                with st.spinner("AI is analyzing your interview... This may take 5-7 minutes."):
                    progress_bar = st.progress(0)
                    
                    progress_bar.progress(50) 
                    results = run_full_pipeline(audio_path)
                    st.session_state.analysis_results = results
                    st.session_state.analysis_complete = True
                    progress_bar.progress(100)
                
                st.success("Analysis completed successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error analyzing interview: {str(e)}")
            finally:
                if os.path.exists(audio_path):
                    os.unlink(audio_path)
    
    # Display results if analysis is complete
    if st.session_state.analysis_complete and st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "Dashboard", "AI Evaluation", "Skills Analysis", "Transcript"
        ])
        
        with tab1:
            st.markdown('<div class="fade-in">', unsafe_allow_html=True)
            st.markdown("""
            <div class="custom-card" style="width: 100%; text-align: center;">
                <h3 style="color: #667eea; text-align: center; margin: 0;">
                    Interview Overview Dashboard
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Duration</h3>
                    <h2>{results['audio_metadata']['duration']:.1f}</h2>
                    <small>seconds</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                sentiment = results['sentiment']
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Sentiment</h3>
                    <h2>{sentiment['label'].title()}</h2>
                    <small>Score: {sentiment['score']:.2f}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                skills_count = len(results['skills_info']['skills'])
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Skills</h3>
                    <h2>{skills_count}</h2>
                    <small>Detected</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                segments_count = len(results['diarized_segments'])
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Segments</h3>
                    <h2>{segments_count}</h2>
                    <small>Conversation</small>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab4:
            st.markdown("""
            <div class="custom-card" style="width: 100%; text-align: center;">
                <h3 style="color: #667eea; text-align: center; margin: 0;">
                    Conversation Transcript
                </h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("**Speaker Legend:** 🔵 Candidate | 🔴 Interviewer")
            
            for segment in results['diarized_segments']:
                speaker_class = "Candidate" if segment['speaker'] == results['candidate_speaker'] else "Interviewer"
                speaker_emoji = "🔵" if segment['speaker'] == results['candidate_speaker'] else "🔴"
                
                st.markdown(f"""
                <div class="transcript-segment {speaker_class}">
                    <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 0.5rem;">
                        <strong>{speaker_emoji} {speaker_class} : &nbsp</strong>
                        <small style="color: #666;">{segment['start']:.1f}s - {segment['end']:.1f}s</small>
                    </div>
                    <div style="color: #333;">{segment['text']}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
            <div class="custom-card" style="width: 100%; text-align: center;">
                <h3 style="color: #667eea; text-align: center; margin: 0;">
                    Skills & Qualifications Analysis
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            skills_info = results['skills_info']
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Skill Summary:")
                if skills_info['skills']:
                    skills_html = ' '.join([f'<span class="skill-item">{skill}</span>' for skill in skills_info['skills']])
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.info("No technical skills detected")
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.subheader("Languages:")
                if skills_info['languages']:
                    languages_html = ' '.join([f'<span class="skill-item">{lang}</span>' for lang in skills_info['languages']])
                    st.markdown(languages_html, unsafe_allow_html=True)
                else:
                    st.info("No languages detected")
                st.markdown("</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:    
                st.subheader("Tools & Software:")
                if skills_info['tools']:
                    tools_html = ' '.join([f'<span class="skill-item">{tool}</span>' for tool in skills_info['tools']])
                    st.markdown(tools_html, unsafe_allow_html=True)
                else:
                    st.info("No tools detected")
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:    
                st.subheader("Education:")
                if skills_info['degrees']:
                    degrees_html = ' '.join([f'<span class="skill-item">{degree}</span>' for degree in skills_info['degrees']])
                    st.markdown(degrees_html, unsafe_allow_html=True)
                else:
                    st.info("No education information detected")
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="fade-in">', unsafe_allow_html=True)
            st.markdown("""
            <div class="custom-card" style="width: 100%; text-align: center;">
                <h3 style="color: #667eea; text-align: center; margin: 0;">
                    AI Evaluation & Recommendation
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.text_area(
                "Evaluation Details",
                results['evaluation'],
                height=600,
                key="evaluation_display",
                label_visibility="collapsed"
            )
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Download Section
        st.markdown("---")
        st.markdown("""
        <div class="fade-in">
            <h2>Download Professional Reports</h2>
            <p>Export comprehensive analysis in your preferred format</p>
        </div>
        """, unsafe_allow_html=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"professional_interview_analysis_{timestamp}"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            txt_data = ""
            try:
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
                    export_txt(results, tmp_file.name)
                    with open(tmp_file.name, 'r', encoding='utf-8') as f:
                        txt_data = f.read()
                os.unlink(tmp_file.name)
            except Exception as e:
                txt_data = f"Error generating TXT: {str(e)}"
            
            st.download_button(
                label="Download TXT Report",
                data=txt_data,
                file_name=f"{default_name}.txt",
                mime="text/plain",
                use_container_width=True,
                key="download_txt"
            )
        
        with col2:
            json_data = ""
            try:
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
                    export_json(results, tmp_file.name)
                    with open(tmp_file.name, 'r', encoding='utf-8') as f:
                        json_data = f.read()
                os.unlink(tmp_file.name)
            except Exception as e:
                json_data = json.dumps({"error": f"Error generating JSON: {str(e)}"})
            
            st.download_button(
                label="Download JSON Report",
                data=json_data,
                file_name=f"{default_name}.json",
                mime="application/json",
                use_container_width=True,
                key="download_json"
            )
        
        with col3:
            pdf_data = b""
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    export_pdf(results, tmp_file.name)
                    with open(tmp_file.name, 'rb') as f:
                        pdf_data = f.read()
                os.unlink(tmp_file.name)
            except Exception as e:
                try:
                    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
                        export_txt(results, tmp_file.name)
                        with open(tmp_file.name, 'r', encoding='utf-8') as f:
                            pdf_data = f.read().encode('utf-8')
                    os.unlink(tmp_file.name)
                except:
                    pdf_data = f"Error generating PDF: {str(e)}".encode('utf-8')
            
            st.download_button(
                label="Download PDF Report",
                data=pdf_data,
                file_name=f"{default_name}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf"
            )
    
    else:
        if not st.session_state.analysis_complete:
            st.markdown("""
            <div class="fade-in" style="text-align: center; padding: 3rem 1rem;">
                <h2 style="color: #667eea;">Ready to Analyze Your Interview?</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="custom-card" style="text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <h4>Accurate Transcription</h4>
                    <p style="font-size: 0.9rem;">Powered by OpenAI Whisper</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="custom-card" style="text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <h4>Smart Diarization</h4>
                    <p style="font-size: 0.9rem;">Automatically identify speakers</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="custom-card" style="text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <h4>Sentiment Analysis</h4>
                    <p style="font-size: 0.9rem;">Understand emotional tone</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="custom-card" style="text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <h4>Skills Extraction</h4>
                    <p style="font-size: 0.9rem;">Detect technical skills</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="fade-in" style="text-align: center; padding: 3rem 1rem;">
                <h2 style="color: #667eea;">How it works:</h2>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown("""
                <div class="custom-card" style="text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <h4>Upload Audio</h4>
                    <p style="font-size: 0.9rem;">Upload your interview audio file in MP3, WAV, or M4A format</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class="custom-card" style="text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <h4>AI Analysis</h4>
                    <p style="font-size: 0.9rem;">Our AI processes with transcription and comprehensive analysis</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown("""
                <div class="custom-card" style="text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <h4>Review Insights</h4>
                    <p style="font-size: 0.9rem;">Explore comprehensive insights in interactive dashboard</p>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown("""
                <div class="custom-card" style="text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <h4>Get Reports</h4>
                    <p style="font-size: 0.9rem;">Download professional reports in multiple file formats</p>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()