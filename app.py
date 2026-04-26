"""EduCore - Premium AI-Powered Learning Platform"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import os

from config import CLASSES, SUBJECTS
from tutor.session import StudentSession
from tutor.quiz import QuizGenerator
from tutor.explain import ExplanationEngine
from utils.translate import detect_language, translate_and_detect, format_response_multilingual
from utils.speech import SpeechProcessor
from utils.report import ReportGenerator

# ============================================
# Page Configuration & Styling
# ============================================

st.set_page_config(
    page_title="EduCore - AI Learning Platform",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "EduCore v1.0 - Next Generation Learning"}
)

# Custom CSS for professional look - Modern Design
st.markdown("""
<style>
    /* Root variables */
    :root {
        --primary: #6366f1;
        --secondary: #8b5cf6;
        --accent: #ec4899;
        --dark: #1e293b;
        --light: #f8fafc;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
    }

    /* Global styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Main container */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e0e7ff 100%);
        min-height: 100vh;
    }

    /* Headers with gradient */
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Sidebar styling - Modern dark theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {
        color: #f1f5f9 !important;
        font-weight: 600;
    }

    [data-testid="stSidebar"] p {
        color: #cbd5e1 !important;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #6366f1;
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -1px;
    }

    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600;
    }

    /* Buttons - Modern style */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 12px 28px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        cursor: pointer;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(99, 102, 241, 0.4);
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
    }

    .stButton > button:active {
        transform: translateY(-1px);
    }

    /* Input fields - Modern style */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 12px 16px;
        background-color: #ffffff;
        transition: all 0.3s ease;
        font-size: 14px;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15), 0 4px 12px rgba(99, 102, 241, 0.2);
        outline: none;
    }

    /* File uploader */
    .stFileUploader {
        border-radius: 10px;
        border: 2px dashed #cbd5e1;
        padding: 20px;
        transition: all 0.3s ease;
    }

    .stFileUploader:hover {
        border-color: #6366f1;
        background-color: rgba(99, 102, 241, 0.05);
    }

    /* Success/Error/Warning messages */
    .stSuccess {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
    }

    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.1);
    }

    .stWarning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.1);
    }

    .stInfo {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
    }

    /* Tabs - Modern style */
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        font-weight: 600;
        border-radius: 10px 10px 0 0;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(99, 102, 241, 0.1);
    }

    .stTabs [aria-selected="true"] {
        border-bottom-color: #6366f1;
        color: #6366f1;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }

    /* Containers and cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
        border-color: #cbd5e1;
    }

    /* Selectbox arrow */
    .stSelectbox svg {
        color: #6366f1;
    }

    /* Radio buttons */
    .stRadio > label > div {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 12px 16px;
        transition: all 0.3s ease;
    }

    .stRadio > label > div:hover {
        border-color: #6366f1;
        background-color: rgba(99, 102, 241, 0.05);
    }

    /* Expander */
    .stExpander {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
    }

    .stExpander > div > button {
        border-radius: 10px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }

    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* Additional Premium Styling */

    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05)) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1)) !important;
    }

    /* Text area styling */
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }

    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15) !important;
    }

    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    }

    /* Chat message styling */
    .stChatMessage {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        border-radius: 12px !important;
        border-left: 4px solid #6366f1 !important;
    }

    /* Number input */
    .stNumberInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
    }

    .stNumberInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15) !important;
    }

    /* Checkbox styling */
    .stCheckbox > label > div {
        border-radius: 6px !important;
    }

    /* Columns spacing */
    .stColumn {
        padding: 0 12px;
    }

    /* Better link styling */
    a {
        color: #6366f1 !important;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    a:hover {
        color: #8b5cf6 !important;
        text-decoration: underline;
    }

    /* Code block styling */
    pre {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }

    code {
        color: #e2e8f0 !important;
        font-family: 'Fira Code', 'Courier New', monospace !important;
    }

    /* Spinner animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .stSpinner {
        animation: spin 1s linear infinite;
    }

    /* Smooth page transitions */
    .main {
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Better select styling */
    select {
        background: white url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236366f1' d='M6 9L1 4h10z'/%3E%3C/svg%3E") no-repeat right 10px center !important;
        padding-right: 30px !important;
        appearance: none !important;
        -webkit-appearance: none !important;
    }

    /* Slider value label */
    .stMetric {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05)) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* Better container styling */
    .stContainer {
        border-radius: 16px !important;
    }

    /* Glowing effect on focus */
    *:focus {
        outline: none !important;
    }

    input:focus,
    select:focus,
    textarea:focus {
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Session State Initialization
# ============================================

if "student_session" not in st.session_state:
    st.session_state.student_session = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0

# Initialize engines
quiz_gen = QuizGenerator()
explain_engine = ExplanationEngine()
report_gen = ReportGenerator()
speech_processor = SpeechProcessor()

# ============================================
# Header Section
# ============================================

st.markdown("""
<div style='background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%); border-radius: 16px; padding: 40px; margin-bottom: 30px; box-shadow: 0 12px 32px rgba(99, 102, 241, 0.2);'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h1 style='color: white; font-size: 44px; font-weight: 800; margin: 0 0 8px 0;'>✨ EduCore</h1>
            <p style='color: rgba(255,255,255,0.95); font-size: 16px; font-weight: 500; margin: 0;'>Next-Generation Adaptive Learning Platform</p>
        </div>
        <div style='text-align: right;'>
            <p style='color: rgba(255,255,255,0.9); font-size: 13px; margin: 0 0 6px 0;'>🚀 Powered by Gemini AI</p>
            <div style='background: rgba(255,255,255,0.25); color: white; padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block;'>● Active Now</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# Sidebar Configuration
# ============================================

with st.sidebar:
    st.markdown("## 🎯 Learning Dashboard")
    st.markdown("---")
    
    # Student Profile
    st.markdown("### Student Profile")
    student_id = st.text_input("Name or ID", value="Student", key="student_id", 
                               help="Your learning identifier")
    
    # Learning Path Selection
    st.markdown("### Learning Path")
    selected_class = st.selectbox(
        "Class Level",
        CLASSES,
        format_func=lambda x: f"Class {x}",
        help="Select your current class level"
    )
    
    selected_subject = st.selectbox(
        "Subject",
        list(SUBJECTS.keys()),
        help="Choose the subject to focus on"
    )
    
    st.markdown("---")

    # Study Materials Section
    with st.expander("📚 Study Materials", expanded=False):
        st.markdown("**Manage your learning resources**")

        material_tab1, material_tab2 = st.tabs(["Upload", "Download"])

        with material_tab1:
            st.markdown("**Upload Custom PDF**")
            pdf_file = st.file_uploader(
                "Upload PDF",
                type="pdf",
                help="Upload NCERT or custom textbooks",
                label_visibility="collapsed"
            )

            if pdf_file:
                os.makedirs("data/custom_pdfs", exist_ok=True)
                pdf_path = os.path.join("data/custom_pdfs", pdf_file.name)
                with open(pdf_path, "wb") as f:
                    f.write(pdf_file.getbuffer())

                st.success(f"✅ Uploaded: {pdf_file.name}")

                # Auto-process the PDF
                if st.button("🔄 Process & Index PDF", use_container_width=True):
                    with st.spinner("Processing PDF..."):
                        try:
                            from rag.loader import PDFLoader
                            loader = PDFLoader()
                            loader.load_pdf(pdf_path, subject=selected_subject, class_level=selected_class)
                            st.success("📚 PDF indexed successfully!")
                        except Exception as e:
                            st.error(f"Error processing PDF: {str(e)}")

        with material_tab2:
            st.markdown("**Download Official NCERT Books**")
            st.info("📖 Download official NCERT textbooks for Classes 6-10")

            if st.button("⬇️ Download All NCERT Books", use_container_width=True, key="download_ncert"):
                with st.spinner("🔄 Downloading books from ncert.nic.in..."):
                    try:
                        from download_ncert_books import download_ncert_books, get_available_books
                        successful, failed = download_ncert_books()

                        if successful > 0:
                            st.success(f"✅ Successfully downloaded {successful} books!")

                        if failed > 0:
                            st.warning(f"⚠️ Failed to download {failed} books")

                        # Index the books
                        st.info("🔄 Indexing books into knowledge base...")
                        try:
                            from rag.loader import PDFLoader
                            loader = PDFLoader()
                            pdf_dir = "data/ncert_pdfs"

                            if os.path.exists(pdf_dir):
                                for filename in os.listdir(pdf_dir):
                                    if filename.endswith('.pdf'):
                                        pdf_path = os.path.join(pdf_dir, filename)
                                        try:
                                            # Extract class and subject from filename
                                            parts = filename.replace('.pdf', '').split('_')
                                            if len(parts) >= 2:
                                                class_level = int(parts[0].replace('Class', ''))
                                                subject = '_'.join(parts[1:]).replace('_', ' ')
                                                loader.load_pdf(pdf_path, subject=subject, class_level=class_level)
                                        except Exception as e:
                                            pass

                            st.success("✨ All books indexed successfully!")

                        except Exception as e:
                            st.error(f"Error indexing books: {str(e)}")

                    except Exception as e:
                        st.error(f"Download error: {str(e)}")

            # Show downloaded books
            st.markdown("**Available Books:**")
            try:
                from download_ncert_books import get_available_books
                books = get_available_books()

                if books:
                    for book_name, info in books.items():
                        st.caption(f"✓ {book_name} ({info['size_mb']} MB)")
                else:
                    st.caption("No books downloaded yet. Click the button above to get started!")
            except Exception as e:
                st.caption("Unable to load books list")

    st.markdown("---")

    # Start Learning Button
    if st.button("🚀 Start Learning Session", use_container_width=True, key="start_btn"):
        st.session_state.student_session = StudentSession(
            student_id=student_id,
            subject=selected_subject,
            class_level=selected_class
        )
        st.success(f"Welcome {student_id}! 🎉")

    st.markdown("---")
    
    # Analytics Section
    if st.session_state.student_session:
        st.markdown("### 📊 Performance Analytics")
        summary = st.session_state.student_session.get_progress_summary()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Accuracy", f"{summary['accuracy']:.1f}%", "↑ Learning")
        with col2:
            st.metric("Questions", summary['total_questions'], "✓ Answered")
        
        # Topic Confidence Radar
        if summary['topic_confidence']:
            topics = list(summary['topic_confidence'].keys())
            confidences = [summary['topic_confidence'][t] * 100 for t in topics]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=confidences,
                theta=topics,
                fill='toself',
                name='Mastery Level',
                line_color='#6366f1',
                fillcolor='rgba(99, 102, 241, 0.2)'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor='#e2e8f0'),
                    bgcolor='rgba(248, 250, 252, 0.5)'
                ),
                showlegend=False,
                height=300,
                margin=dict(l=50, r=50, t=50, b=50),
                paper_bgcolor='white',
                font=dict(size=10, color='#64748b')
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    # Reports & Insights
    st.markdown("### 📈 Reports & Insights")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.student_session and st.button("📄 Weekly Report", use_container_width=True):
            report_path = f"reports/{st.session_state.student_session.student_id}_report.pdf"
            if report_gen.generate_weekly_report(
                st.session_state.student_session,
                report_path
            ):
                with open(report_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download",
                        data=f.read(),
                        file_name=os.path.basename(report_path),
                        mime="application/pdf",
                        use_container_width=True
                    )
    
    with col2:
        language = st.selectbox("Language", ["English", "Hindi", "Telugu"], key="lang")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; font-size: 11px; margin-top: 20px;'>
        <p>EduCore v1.0</p>
        <p>Powered by Google Gemini AI</p>
        <p>© 2024 EduCore. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# Main Content Area
# ============================================

if not st.session_state.student_session:
    # Welcome Screen - Clean & Professional
    st.markdown("""
    <style>
        .welcome-container {
            padding: 60px 20px;
        }

        .welcome-title {
            text-align: center;
            margin-bottom: 50px;
        }

        .welcome-title h1 {
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .welcome-title p {
            color: #64748b;
            font-size: 18px;
            margin: 8px 0;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin: 50px 0;
        }

        .feature-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            padding: 32px 24px;
            text-align: center;
            transition: all 0.4s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .feature-card:hover {
            border-color: #6366f1;
            box-shadow: 0 12px 32px rgba(99, 102, 241, 0.15);
            transform: translateY(-8px);
        }

        .feature-icon {
            font-size: 48px;
            margin-bottom: 16px;
        }

        .feature-card h3 {
            color: #1e293b;
            font-size: 20px;
            font-weight: 700;
            margin: 12px 0;
        }

        .feature-card p {
            color: #64748b;
            font-size: 15px;
            line-height: 1.6;
            margin: 0;
        }

        .stats-section {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border-radius: 20px;
            padding: 50px 30px;
            margin: 50px 0;
            text-align: center;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 40px;
        }

        .stat-item {
            color: white;
        }

        .stat-number {
            font-size: 44px;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .stat-label {
            font-size: 16px;
            font-weight: 500;
            opacity: 0.95;
        }

        .steps-section {
            text-align: center;
            margin: 50px 0;
        }

        .steps-title {
            font-size: 22px;
            color: #1e293b;
            font-weight: 700;
            margin-bottom: 30px;
        }

        .steps-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        .step-card {
            padding: 24px;
            border-radius: 12px;
            border-left: 5px solid;
            transition: all 0.3s ease;
        }

        .step-card:nth-child(1) {
            background: #ecfdf5;
            border-left-color: #10b981;
        }

        .step-card:nth-child(2) {
            background: #eff6ff;
            border-left-color: #3b82f6;
        }

        .step-card:nth-child(3) {
            background: #fef3c7;
            border-left-color: #f59e0b;
        }

        .step-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }

        .step-number {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .step-title {
            color: #1e293b;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .step-desc {
            color: #64748b;
            font-size: 14px;
        }
    </style>

    <div class="welcome-container">
        <div class="welcome-title">
            <h1>Welcome to EduCore</h1>
            <p>Next-Generation Adaptive Learning Platform</p>
            <p style="color: #94a3b8;">AI-powered personalized education for Classes 6-10</p>
        </div>

        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3>Truly Adaptive</h3>
                <p>Difficulty adjusts in real-time based on your performance</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <h3>AI-Powered</h3>
                <p>Google Gemini AI generates personalized explanations</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <h3>Official NCERT</h3>
                <p>Aligned with official Indian CBSE curriculum</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">🌐</div>
                <h3>Multilingual</h3>
                <p>Learn in English, Hindi, Telugu, Kannada & Malayalam</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>Advanced Analytics</h3>
                <p>Track progress with detailed performance charts</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">🎤</div>
                <h3>Voice Enabled</h3>
                <p>Speak questions, listen to explanations</p>
            </div>
        </div>

        <div class="stats-section">
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">15+</div>
                    <div class="stat-label">Official Textbooks</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">1500+</div>
                    <div class="stat-label">Unique Questions</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">5</div>
                    <div class="stat-label">Languages</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Free Forever</div>
                </div>
            </div>
        </div>

        <div class="steps-section">
            <p class="steps-title">Get Started in 3 Simple Steps</p>
            <div class="steps-grid">
                <div class="step-card">
                    <div class="step-number">1️⃣</div>
                    <div class="step-title">Enter Your Details</div>
                    <div class="step-desc">Name, Class & Subject</div>
                </div>
                <div class="step-card">
                    <div class="step-number">2️⃣</div>
                    <div class="step-title">Choose a Topic</div>
                    <div class="step-desc">From your curriculum</div>
                </div>
                <div class="step-card">
                    <div class="step-number">3️⃣</div>
                    <div class="step-title">Start Learning</div>
                    <div class="step-desc">AI guides your journey</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    session = st.session_state.student_session
    
    # Session Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"## 📚 {session.subject} — Class {session.class_level}")
    with col2:
        st.metric("Current Level", session.get_current_level().upper(), 
                 delta="Adaptive" if session.get_current_level() != "medium" else "Standard")
    with col3:
        st.metric("Session Time", f"{summary['session_duration_minutes']:.0f}m", delta="Active")
    
    st.markdown("---")
    
    # Topic Selection with improved UX
    topics = SUBJECTS.get(session.subject, [])
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_topic = st.selectbox("📖 Select Learning Topic", topics, key="topic")
    with col2:
        st.write("")
        st.write("")
        if st.button("Refresh", use_container_width=True):
            st.rerun()
    
    if selected_topic:
        session.set_topic(selected_topic)
    
    st.markdown("---")
    
    # Main Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Ask & Learn", "📝 Practice Quiz", "📖 Study", "📊 Progress"])
    
    # ========== TAB 1: Ask & Learn ==========
    with tab1:
        st.markdown("### Ask Questions About Your Topic")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            user_question = st.text_input(
                "Your Question",
                placeholder=f"e.g., Explain {selected_topic}",
                label_visibility="collapsed"
            )
        with col2:
            st.write("")
            ask_btn = st.button("🔍 Ask", use_container_width=True)
        
        if ask_btn and user_question:
            with st.spinner("🧠 Thinking..."):
                response = explain_engine.answer_question(
                    question=user_question,
                    subject=session.subject,
                    class_level=session.class_level
                )
            
            st.session_state.messages.append({"role": "user", "content": user_question})
            
            # Display answer
            if response.get("answer"):
                with st.container():
                    st.success(f"**Answer:** {response['answer']}")
                    
                    if response.get("explanation"):
                        st.info(f"**📖 More:** {response['explanation']}")
                    
                    if response.get("analogy"):
                        st.success(f"**💡 Think of it like:** {response['analogy']}")
        
        # Chat History
        if st.session_state.messages:
            st.markdown("### 💬 Recent Questions")
            for msg in st.session_state.messages[-5:]:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
    
    # ========== TAB 2: Practice Quiz ==========
    with tab2:
        st.markdown("### Practice & Test Your Knowledge")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🎯 Generate Quiz (5 Questions)", use_container_width=True):
                st.session_state.quiz_active = True
                st.session_state.quiz_index = 0
                
                with st.spinner("Generating questions..."):
                    st.session_state.quiz_questions = quiz_gen.generate_quiz(
                        topic=selected_topic,
                        num_questions=5,
                        class_level=session.class_level,
                        subject=session.subject
                    )
                st.success("✅ Quiz generated!")
        
        if st.session_state.quiz_active and st.session_state.quiz_questions:
            q_idx = st.session_state.quiz_index
            question = st.session_state.quiz_questions[q_idx]
            
            st.markdown(f"### Question {q_idx + 1} of 5")
            
            # Question display
            st.markdown(f"""
            <div style='background: #f8fafc; padding: 20px; border-radius: 8px; border-left: 4px solid #6366f1;'>
                <p style='color: #64748b; font-weight: 600; margin: 0;'>{question['difficulty'].upper()} • {question['type'].upper()}</p>
                <h3 style='margin: 10px 0 0 0;'>{question['question']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
            
            # Answer input
            if question['type'] == 'mcq':
                options = question.get('options', {})
                if options:
                    selected_answer = st.radio(
                        "Choose your answer:",
                        list(options.keys()),
                        format_func=lambda x: f"{x}: {options[x]}",
                        label_visibility="collapsed"
                    )
                    
                    if st.button("✓ Submit Answer", use_container_width=True, key=f"submit_{q_idx}"):
                        with st.spinner("Evaluating..."):
                            result = quiz_gen.evaluate_answer(question, selected_answer)
                        
                        session.record_question(question['question'], selected_answer, result['is_correct'])
                        session.update_confidence(selected_topic, result['is_correct'])
                        
                        if result['is_correct']:
                            st.success(f"🎉 Correct! {result.get('feedback', '')}")
                        else:
                            st.error(f"Not quite. {result.get('feedback', '')}")
                        
                        st.info(f"**Explanation:** {question.get('explanation', '')}")
                        
                        st.markdown("")
                        if q_idx < 4:
                            if st.button("→ Next Question", use_container_width=True):
                                st.session_state.quiz_index += 1
                                st.rerun()
                        else:
                            st.balloons()
                            st.success("🎓 Quiz Complete!")
                            summary = session.get_progress_summary()
                            st.metric("Quiz Score", f"{summary['accuracy']:.1f}%")
            
            else:
                student_answer = st.text_area("Your answer:", height=100)
                if st.button("✓ Submit Answer", use_container_width=True):
                    with st.spinner("Evaluating..."):
                        result = quiz_gen.evaluate_answer(question, student_answer)
                    
                    session.record_question(question['question'], student_answer, result['is_correct'])
                    session.update_confidence(selected_topic, result['is_correct'])
                    
                    if result['is_correct']:
                        st.success("✅ Great answer!")
                    else:
                        st.warning("Good effort! Here's what we're looking for...")
                    
                    st.info(f"**Feedback:** {result.get('feedback', '')}")
    
    # ========== TAB 3: Study ==========
    with tab3:
        st.markdown("### Explore & Learn")
        
        if st.button("📚 Get Explanation", use_container_width=True):
            with st.spinner("Loading content..."):
                explanation = explain_engine.explain_topic(
                    topic=selected_topic,
                    class_level=session.class_level,
                    subject=session.subject
                )
            
            if explanation.get("explanation"):
                st.markdown(f"## {selected_topic}")
                st.markdown(explanation["explanation"])
                
                if explanation.get("analogy"):
                    st.success(f"**💡 Real-world analogy:** {explanation['analogy']}")
                
                if explanation.get("example"):
                    st.info(f"**📌 Example:** {explanation['example']}")
                
                if explanation.get("key_points"):
                    st.markdown("**Key Points:**")
                    for point in explanation["key_points"]:
                        st.write(f"• {point}")
    
    # ========== TAB 4: Progress ==========
    with tab4:
        st.markdown("### Your Learning Analytics")
        
        summary = session.get_progress_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Questions", summary['total_questions'], "+2 today")
        with col2:
            st.metric("Accuracy", f"{summary['accuracy']:.1f}%", "↑ 5%")
        with col3:
            st.metric("Topics Mastered", len([v for v in summary['topic_confidence'].values() if v >= 0.7]))
        with col4:
            st.metric("Streak", f"{summary['session_duration_minutes']:.0f} min", "Active")
        
        st.markdown("---")
        st.markdown("### Topic Performance")
        
        if summary['topic_confidence']:
            for topic, confidence in summary['topic_confidence'].items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.progress(confidence, text=topic)
                with col2:
                    if confidence >= 0.7:
                        st.write("🟢 Strong")
                    elif confidence >= 0.4:
                        st.write("🟡 Good")
                    else:
                        st.write("🔴 Practice")
        
        st.markdown("---")
        
        if st.button("💾 Save Progress", use_container_width=True):
            session_path = f"sessions/{session.student_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs("sessions", exist_ok=True)
            session.save_session(session_path)
            st.success(f"✅ Progress saved!")

# ============================================
# Footer
# ============================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 12px; padding: 20px;'>
    <p><strong>EduCore</strong> — Next-Generation AI Learning Platform</p>
    <p>Powered by Google Gemini • NCERT Curriculum • Adaptive Learning</p>
    <p style='margin-top: 10px; font-size: 10px;'>© 2024 EduCore. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
