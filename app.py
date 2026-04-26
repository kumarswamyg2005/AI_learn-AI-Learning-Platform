"""EduCore — Intelligent Learning Platform"""

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

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduCore",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# DESIGN SYSTEM  (full professional CSS)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ═══════════════════════════════════════════════════════════
   FONTS
═══════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ═══════════════════════════════════════════════════════════
   APP SHELL
═══════════════════════════════════════════════════════════ */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #f5f6fa !important;
    color: #111827 !important;
}

/* Remove Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Main content wrapper */
.main .block-container {
    padding: 2rem 2.5rem 3rem 2.5rem !important;
    max-width: 1280px !important;
    background: #f5f6fa;
}

/* ═══════════════════════════════════════════════════════════
   SIDEBAR  (dark navy)
═══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1c2333 !important;
    padding-top: 0 !important;
}
/* Kill every default colour inside sidebar */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #c9d1d9 !important;
    -webkit-text-fill-color: #c9d1d9 !important;
}
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #6e7681 !important;
    -webkit-text-fill-color: #6e7681 !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid #1c2333 !important;
    margin: 12px 0 !important;
}

/* Sidebar inputs */
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: #484f58 !important;
}
[data-testid="stSidebar"] .stSelectbox svg {
    fill: #8b949e !important;
}

/* Sidebar expander */
[data-testid="stSidebar"] .stExpander {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stExpander summary {
    color: #c9d1d9 !important;
}

/* ═══════════════════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════════════════ */
.stButton > button {
    background: #4f46e5 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    padding: 9px 18px !important;
    line-height: 1.4 !important;
    letter-spacing: 0.01em !important;
    transition: background 0.18s ease, box-shadow 0.18s ease, transform 0.12s ease !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08) !important;
    cursor: pointer !important;
    -webkit-text-fill-color: #ffffff !important;
}
.stButton > button:hover {
    background: #4338ca !important;
    box-shadow: 0 4px 14px rgba(79,70,229,0.38) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 1px 4px rgba(79,70,229,0.2) !important;
}

/* ═══════════════════════════════════════════════════════════
   INPUTS & TEXTAREAS
═══════════════════════════════════════════════════════════ */
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    color: #111827 !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.15) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: #9ca3af !important;
}
.stTextArea > div > div > textarea {
    background: #ffffff !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    color: #111827 !important;
    font-family: 'Inter', sans-serif !important;
    resize: vertical !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.15) !important;
    outline: none !important;
}

/* ═══════════════════════════════════════════════════════════
   SELECTBOX
═══════════════════════════════════════════════════════════ */
.stSelectbox > div > div {
    background: #ffffff !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 8px !important;
    color: #111827 !important;
    font-size: 14px !important;
    transition: border-color 0.18s !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.15) !important;
}
.stSelectbox [data-baseweb="select"] span {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-size: 14px !important;
}

/* ═══════════════════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 2px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 7px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    color: #6b7280 !important;
    -webkit-text-fill-color: #6b7280 !important;
    transition: all 0.18s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: #f3f4f6 !important;
    color: #374151 !important;
    -webkit-text-fill-color: #374151 !important;
}
.stTabs [aria-selected="true"] {
    background: #4f46e5 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(79,70,229,0.28) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 20px !important;
}

/* ═══════════════════════════════════════════════════════════
   METRIC CARDS
═══════════════════════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}
[data-testid="stMetricLabel"] > div {
    color: #6b7280 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    -webkit-text-fill-color: #6b7280 !important;
}
[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    -webkit-text-fill-color: #111827 !important;
}
[data-testid="stMetricDelta"] {
    color: #059669 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    -webkit-text-fill-color: #059669 !important;
}

/* ═══════════════════════════════════════════════════════════
   ALERTS / NOTIFICATIONS
═══════════════════════════════════════════════════════════ */
/* Success */
[data-testid="stAlert"][kind="success"],
div[data-baseweb="notification"][kind="positive"] {
    background: #f0fdf4 !important;
    border: 1px solid #bbf7d0 !important;
    border-radius: 10px !important;
}
[data-testid="stAlert"][kind="success"] p,
[data-testid="stAlert"][kind="success"] div {
    color: #15803d !important;
    -webkit-text-fill-color: #15803d !important;
}
/* Error */
[data-testid="stAlert"][kind="error"] {
    background: #fef2f2 !important;
    border: 1px solid #fecaca !important;
    border-radius: 10px !important;
}
[data-testid="stAlert"][kind="error"] p,
[data-testid="stAlert"][kind="error"] div {
    color: #dc2626 !important;
    -webkit-text-fill-color: #dc2626 !important;
}
/* Warning */
[data-testid="stAlert"][kind="warning"] {
    background: #fffbeb !important;
    border: 1px solid #fde68a !important;
    border-radius: 10px !important;
}
[data-testid="stAlert"][kind="warning"] p,
[data-testid="stAlert"][kind="warning"] div {
    color: #b45309 !important;
    -webkit-text-fill-color: #b45309 !important;
}
/* Info */
[data-testid="stAlert"][kind="info"] {
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 10px !important;
}
[data-testid="stAlert"][kind="info"] p,
[data-testid="stAlert"][kind="info"] div {
    color: #1d4ed8 !important;
    -webkit-text-fill-color: #1d4ed8 !important;
}

/* ═══════════════════════════════════════════════════════════
   PROGRESS BAR
═══════════════════════════════════════════════════════════ */
.stProgress > div > div {
    background: #e5e7eb !important;
    border-radius: 99px !important;
    height: 8px !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
    border-radius: 99px !important;
    box-shadow: 0 0 8px rgba(79,70,229,0.4) !important;
}
/* Progress text */
.stProgress p {
    color: #374151 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    -webkit-text-fill-color: #374151 !important;
}

/* ═══════════════════════════════════════════════════════════
   RADIO BUTTONS
═══════════════════════════════════════════════════════════ */
.stRadio > div {
    gap: 8px !important;
}
.stRadio label {
    background: #ffffff !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    cursor: pointer !important;
    transition: all 0.18s !important;
    width: 100% !important;
}
.stRadio label:hover {
    border-color: #4f46e5 !important;
    background: #eef2ff !important;
}
.stRadio label span {
    color: #374151 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    -webkit-text-fill-color: #374151 !important;
}

/* ═══════════════════════════════════════════════════════════
   FILE UPLOADER
═══════════════════════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 2px dashed #d1d5db !important;
    border-radius: 10px !important;
    padding: 12px !important;
    transition: border-color 0.18s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #4f46e5 !important;
}
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span {
    color: #6b7280 !important;
    -webkit-text-fill-color: #6b7280 !important;
}

/* ═══════════════════════════════════════════════════════════
   EXPANDERS  (main content)
═══════════════════════════════════════════════════════════ */
.stExpander {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
.stExpander summary {
    color: #111827 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    -webkit-text-fill-color: #111827 !important;
}

/* ═══════════════════════════════════════════════════════════
   HEADINGS  (main content only, no gradient — for readability)
═══════════════════════════════════════════════════════════ */
.main h1, .main h2, .main h3, .main h4 {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 700 !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}
.stMarkdown p {
    color: #374151 !important;
    -webkit-text-fill-color: #374151 !important;
    line-height: 1.65 !important;
}

/* ═══════════════════════════════════════════════════════════
   CAPTION  /  SMALL TEXT
═══════════════════════════════════════════════════════════ */
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #9ca3af !important;
    font-size: 12px !important;
    -webkit-text-fill-color: #9ca3af !important;
}

/* ═══════════════════════════════════════════════════════════
   DIVIDER
═══════════════════════════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid #e5e7eb !important;
    margin: 20px 0 !important;
}

/* ═══════════════════════════════════════════════════════════
   CHAT MESSAGES
═══════════════════════════════════════════════════════════ */
[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatMessage"] p {
    color: #374151 !important;
    -webkit-text-fill-color: #374151 !important;
}

/* ═══════════════════════════════════════════════════════════
   SPINNER TEXT
═══════════════════════════════════════════════════════════ */
.stSpinner > div > div {
    border-top-color: #4f46e5 !important;
}
[data-testid="stSpinner"] p {
    color: #6b7280 !important;
    -webkit-text-fill-color: #6b7280 !important;
}

/* ═══════════════════════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #9ca3af; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# REUSABLE HTML COMPONENTS
# ─────────────────────────────────────────────────────────────
def badge(text, color="#4f46e5", bg=None):
    bg = bg or f"{color}18"
    return (f"<span style='display:inline-block;background:{bg};color:{color};"
            f"font-size:11px;font-weight:700;padding:3px 10px;border-radius:99px;"
            f"letter-spacing:0.06em;-webkit-text-fill-color:{color}'>{text}</span>")

def card_html(content, padding="24px", radius="12px", border="#e5e7eb", shadow=True):
    sh = "0 1px 4px rgba(0,0,0,0.07)" if shadow else "none"
    return (f"<div style='background:#fff;border:1px solid {border};border-radius:{radius};"
            f"padding:{padding};box-shadow:{sh};'>{content}</div>")

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
defaults = {
    "student_session": None,
    "messages": [],
    "quiz_active": False,
    "quiz_questions": [],
    "quiz_index": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────
# ENGINES
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_engines():
    return QuizGenerator(), ExplanationEngine(), ReportGenerator(), SpeechProcessor()

quiz_gen, explain_engine, report_gen, speech_proc = load_engines()

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 4px 0;'>
        <div style='font-size:20px;font-weight:800;color:#e6edf3;
                    letter-spacing:-0.4px;margin-bottom:2px'>🎓 EduCore</div>
        <div style='font-size:11px;color:#6e7681;font-weight:500;
                    letter-spacing:0.03em'>Intelligent Learning Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("STUDENT")
    student_id = st.text_input("name", value="Student", key="student_id",
                               placeholder="Your name…",
                               label_visibility="collapsed")

    st.caption("LEARNING PATH")
    selected_class = st.selectbox("class", CLASSES,
                                  format_func=lambda x: f"Class {x}",
                                  label_visibility="collapsed")
    selected_subject = st.selectbox("subject", list(SUBJECTS.keys()),
                                    label_visibility="collapsed")
    st.divider()

    # ── Study Materials ──
    st.caption("STUDY MATERIALS")
    with st.expander("📄 Manage Books"):
        u_tab, d_tab = st.tabs(["Upload PDF", "NCERT Books"])

        with u_tab:
            uploaded = st.file_uploader("pdf", type="pdf",
                                        label_visibility="collapsed")
            if uploaded:
                os.makedirs("data/custom_pdfs", exist_ok=True)
                dest = f"data/custom_pdfs/{uploaded.name}"
                with open(dest, "wb") as fh:
                    fh.write(uploaded.getbuffer())
                st.success(f"Saved · {uploaded.name}")
                if st.button("Index this PDF", use_container_width=True):
                    with st.spinner("Indexing…"):
                        try:
                            from rag.loader import PDFLoader
                            PDFLoader().load_pdf(dest, subject=selected_subject,
                                                 class_level=selected_class)
                            st.success("Done!")
                        except Exception as e:
                            st.error(str(e))

        with d_tab:
            st.caption("Official NCERT textbooks · Classes 6–10")
            if st.button("Download All Books", use_container_width=True):
                with st.spinner("Downloading…"):
                    try:
                        from download_ncert_books import download_ncert_books
                        ok, fail = download_ncert_books(verbose=False)
                        st.success(f"{ok} books downloaded!")
                        if fail:
                            st.warning(f"{fail} failed — retry later")
                    except Exception as e:
                        st.error(str(e))
            try:
                from download_ncert_books import get_available_books
                for name, meta in get_available_books().items():
                    st.caption(f"✓ {name} ({meta['size_mb']} MB)")
            except Exception:
                pass

    st.divider()

    if st.button("▶  Start Session", use_container_width=True, key="start_btn"):
        st.session_state.student_session = StudentSession(
            student_id=student_id,
            subject=selected_subject,
            class_level=selected_class,
        )
        st.success(f"Welcome, {student_id}!")

    # ── Live analytics ──
    if st.session_state.student_session:
        sess = st.session_state.student_session
        sm   = sess.get_progress_summary()
        st.divider()
        st.caption("PERFORMANCE")
        c1, c2 = st.columns(2)
        c1.metric("Accuracy", f"{sm['accuracy']:.0f}%")
        c2.metric("Answered", sm["total_questions"])

        if sm["topic_confidence"]:
            tnames = list(sm["topic_confidence"].keys())
            tvals  = [sm["topic_confidence"][t] * 100 for t in tnames]
            fig = go.Figure(go.Scatterpolar(
                r=tvals, theta=tnames, fill="toself",
                line_color="#4f46e5",
                fillcolor="rgba(79,70,229,0.12)",
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 100],
                                   tickfont=dict(size=8, color="#6e7681"),
                                   gridcolor="#1c2333"),
                    angularaxis=dict(tickfont=dict(size=9, color="#8b949e")),
                ),
                showlegend=False,
                height=200,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True,
                            config={"displayModeBar": False})

        st.divider()
        if st.button("⬇  Download Report", use_container_width=True):
            os.makedirs("reports", exist_ok=True)
            rp = f"reports/{sess.student_id}_report.pdf"
            if report_gen.generate_weekly_report(sess, rp):
                with open(rp, "rb") as fh:
                    st.download_button("Save PDF →", fh.read(),
                                       file_name=os.path.basename(rp),
                                       mime="application/pdf",
                                       use_container_width=True)

    st.divider()
    st.caption("EduCore v2.0 · © 2025")

# ─────────────────────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════
#   HOME  (no session)
# ══════════════════════════════════════════════════════════════
if not st.session_state.student_session:

    # ── Hero ──────────────────────────────────────────────────
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #312e81 0%, #4f46e5 45%, #7c3aed 100%);
        border-radius: 16px;
        padding: 60px 52px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    ">
        <!-- subtle texture ring -->
        <div style="
            position:absolute; top:-80px; right:-80px;
            width:360px; height:360px; border-radius:50%;
            background:rgba(255,255,255,0.04);
            pointer-events:none;
        "></div>
        <div style="
            display:inline-block;
            background:rgba(255,255,255,0.15);
            border:1px solid rgba(255,255,255,0.22);
            border-radius:99px;
            padding:5px 16px;
            font-size:11px;
            font-weight:700;
            color:rgba(255,255,255,0.95);
            letter-spacing:0.09em;
            margin-bottom:20px;
        ">✦ POWERED BY GOOGLE GEMINI AI</div>
        <h1 style="
            font-size:48px;
            font-weight:800;
            color:#ffffff;
            margin:0 0 16px 0;
            line-height:1.15;
            letter-spacing:-1px;
            -webkit-text-fill-color:#ffffff;
        ">Learn Smarter.<br>Grow Faster.</h1>
        <p style="
            font-size:17px;
            color:rgba(255,255,255,0.82);
            margin:0 0 28px 0;
            max-width:520px;
            line-height:1.7;
        ">An adaptive platform built on the official CBSE curriculum for Classes 6–10.
        Personalised explanations, instant quizzes, and detailed progress tracking.</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">
            <div style="
                background:rgba(255,255,255,0.14);
                border:1px solid rgba(255,255,255,0.2);
                color:white;
                border-radius:8px;
                padding:8px 18px;
                font-size:13px;
                font-weight:600;
            ">📚 Classes 6–10</div>
            <div style="
                background:rgba(255,255,255,0.14);
                border:1px solid rgba(255,255,255,0.2);
                color:white;
                border-radius:8px;
                padding:8px 18px;
                font-size:13px;
                font-weight:600;
            ">🌐 5 Languages</div>
            <div style="
                background:rgba(255,255,255,0.14);
                border:1px solid rgba(255,255,255,0.2);
                color:white;
                border-radius:8px;
                padding:8px 18px;
                font-size:13px;
                font-weight:600;
            ">💰 100% Free</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Feature cards ──────────────────────────────────────────
    features = [
        ("🎯", "#4f46e5", "Truly Adaptive",
         "Questions and difficulty adjust live based on how you answer."),
        ("🧠", "#7c3aed", "AI Explanations",
         "Every concept explained simply, with real-world analogies."),
        ("📚", "#0ea5e9", "NCERT Aligned",
         "Content sourced from official CBSE textbooks — nothing extra."),
        ("🌐", "#059669", "5 Languages",
         "Study in English, Hindi, Telugu, Kannada, or Malayalam."),
        ("📊", "#f59e0b", "Progress Analytics",
         "Visual dashboards track your mastery across every topic."),
        ("🎤", "#ec4899", "Voice Mode",
         "Ask questions by voice and hear answers read back to you."),
    ]

    cols1 = st.columns(3)
    cols2 = st.columns(3)
    for i, (icon, color, title, desc) in enumerate(features):
        col = cols1[i] if i < 3 else cols2[i - 3]
        with col:
            st.markdown(f"""
            <div style="
                background:#ffffff;
                border:1px solid #e5e7eb;
                border-radius:12px;
                padding:24px 20px;
                margin-bottom:16px;
                border-top:3px solid {color};
                box-shadow:0 1px 4px rgba(0,0,0,0.06);
            ">
                <div style="font-size:28px;margin-bottom:10px">{icon}</div>
                <div style="
                    font-size:15px;
                    font-weight:700;
                    color:#111827;
                    margin-bottom:7px;
                ">{title}</div>
                <div style="
                    font-size:13px;
                    color:#6b7280;
                    line-height:1.6;
                ">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Stats bar ──────────────────────────────────────────────
    st.markdown("""
    <div style="
        background:#ffffff;
        border:1px solid #e5e7eb;
        border-radius:12px;
        padding:32px 40px;
        margin:4px 0 28px 0;
        display:flex;
        justify-content:space-around;
        text-align:center;
        flex-wrap:wrap;
        gap:20px;
        box-shadow:0 1px 4px rgba(0,0,0,0.06);
    ">
        <div>
            <div style="font-size:34px;font-weight:800;color:#4f46e5;letter-spacing:-1px">15+</div>
            <div style="font-size:13px;color:#6b7280;font-weight:500;margin-top:3px">Official Textbooks</div>
        </div>
        <div style="width:1px;background:#e5e7eb;align-self:stretch"></div>
        <div>
            <div style="font-size:34px;font-weight:800;color:#7c3aed;letter-spacing:-1px">1,500+</div>
            <div style="font-size:13px;color:#6b7280;font-weight:500;margin-top:3px">Practice Questions</div>
        </div>
        <div style="width:1px;background:#e5e7eb;align-self:stretch"></div>
        <div>
            <div style="font-size:34px;font-weight:800;color:#059669;letter-spacing:-1px">5</div>
            <div style="font-size:13px;color:#6b7280;font-weight:500;margin-top:3px">Languages Supported</div>
        </div>
        <div style="width:1px;background:#e5e7eb;align-self:stretch"></div>
        <div>
            <div style="font-size:34px;font-weight:800;color:#f59e0b;letter-spacing:-1px">Free</div>
            <div style="font-size:13px;color:#6b7280;font-weight:500;margin-top:3px">Always</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── How to start ───────────────────────────────────────────
    st.markdown("""
    <div style="font-size:18px;font-weight:700;color:#111827;
                margin-bottom:16px">How to get started</div>
    """, unsafe_allow_html=True)

    steps = [
        ("#10b981", "#f0fdf4", "01", "Fill your profile",
         "Enter your name, class, and subject in the left panel."),
        ("#4f46e5", "#eef2ff", "02", "Pick a topic",
         "Choose any topic from the official CBSE curriculum."),
        ("#f59e0b", "#fffbeb", "03", "Start learning",
         "Ask questions, take quizzes, and watch your progress grow."),
    ]
    sc = st.columns(3)
    for col, (color, bg, num, heading, body) in zip(sc, steps):
        with col:
            st.markdown(f"""
            <div style="
                background:{bg};
                border-radius:12px;
                padding:24px;
                border-left:4px solid {color};
                height:130px;
            ">
                <div style="
                    font-size:11px;
                    font-weight:700;
                    color:{color};
                    letter-spacing:0.09em;
                    margin-bottom:8px;
                ">STEP {num}</div>
                <div style="
                    font-size:16px;
                    font-weight:700;
                    color:#111827;
                    margin-bottom:6px;
                ">{heading}</div>
                <div style="
                    font-size:13px;
                    color:#4b5563;
                    line-height:1.55;
                ">{body}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#   LEARNING SESSION
# ══════════════════════════════════════════════════════════════
else:
    session = st.session_state.student_session
    summary = session.get_progress_summary()
    lvl     = session.get_current_level()
    lvl_color = {"easy": "#059669", "medium": "#f59e0b", "hard": "#dc2626"}.get(lvl, "#4f46e5")

    # ── Session header bar ──────────────────────────────────────
    st.markdown(f"""
    <div style="
        background:#ffffff;
        border:1px solid #e5e7eb;
        border-radius:12px;
        padding:18px 28px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:20px;
        box-shadow:0 1px 3px rgba(0,0,0,0.06);
        flex-wrap:wrap;
        gap:16px;
    ">
        <div>
            <div style="font-size:12px;color:#9ca3af;font-weight:600;
                        text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">
                Active Session
            </div>
            <div style="font-size:20px;font-weight:700;color:#111827">
                {session.subject} &nbsp;·&nbsp; Class {session.class_level}
            </div>
        </div>
        <div style="display:flex;gap:32px;text-align:center">
            <div>
                <div style="font-size:22px;font-weight:800;color:#4f46e5;letter-spacing:-0.5px">
                    {summary['accuracy']:.0f}%
                </div>
                <div style="font-size:11px;color:#9ca3af;font-weight:600;text-transform:uppercase">Accuracy</div>
            </div>
            <div>
                <div style="font-size:22px;font-weight:800;color:#111827;letter-spacing:-0.5px">
                    {summary['total_questions']}
                </div>
                <div style="font-size:11px;color:#9ca3af;font-weight:600;text-transform:uppercase">Answered</div>
            </div>
            <div>
                <div style="font-size:22px;font-weight:800;color:{lvl_color};letter-spacing:-0.5px">
                    {lvl.upper()}
                </div>
                <div style="font-size:11px;color:#9ca3af;font-weight:600;text-transform:uppercase">Level</div>
            </div>
            <div>
                <div style="font-size:22px;font-weight:800;color:#111827;letter-spacing:-0.5px">
                    {summary['session_duration_minutes']:.0f}m
                </div>
                <div style="font-size:11px;color:#9ca3af;font-weight:600;text-transform:uppercase">Session</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Topic selector
    topics = SUBJECTS.get(session.subject, [])
    tc1, tc2 = st.columns([5, 1])
    with tc1:
        selected_topic = st.selectbox("Select Topic", topics, key="topic",
                                      label_visibility="visible")
    with tc2:
        st.markdown("<div style='margin-top:28px'/>", unsafe_allow_html=True)
        if st.button("↺ Refresh", use_container_width=True):
            st.rerun()
    if selected_topic:
        session.set_topic(selected_topic)

    st.markdown("<div style='margin-top:8px'/>", unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬  Ask Anything",
        "📝  Practice Quiz",
        "📖  Study Notes",
        "📊  My Progress",
    ])

    # ─── TAB 1 · Ask ──────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div style="margin-bottom:16px">
            <div style="font-size:20px;font-weight:700;color:#111827">Ask Anything</div>
            <div style="font-size:14px;color:#6b7280;margin-top:3px">
                Type any question about your topic and get a clear, simple answer.
            </div>
        </div>
        """, unsafe_allow_html=True)

        q_col, btn_col = st.columns([5, 1])
        with q_col:
            user_q = st.text_input(
                "question",
                placeholder=f"e.g.  What is {selected_topic}? Explain with an example.",
                label_visibility="collapsed",
                key="question_input",
            )
        with btn_col:
            st.markdown("<div style='margin-top:4px'/>", unsafe_allow_html=True)
            ask_btn = st.button("Ask →", use_container_width=True)

        if ask_btn and user_q:
            with st.spinner("Thinking…"):
                resp = explain_engine.answer_question(
                    question=user_q,
                    subject=session.subject,
                    class_level=session.class_level,
                )
            st.session_state.messages.append({"role": "user", "content": user_q})

            if resp.get("answer"):
                st.markdown(f"""
                <div style="
                    background:#eef2ff;
                    border:1px solid #c7d2fe;
                    border-left:4px solid #4f46e5;
                    border-radius:0 10px 10px 0;
                    padding:20px 22px;
                    margin:16px 0 12px 0;
                ">
                    <div style="font-size:11px;font-weight:700;color:#4f46e5;
                                text-transform:uppercase;letter-spacing:0.07em;margin-bottom:8px">
                        Answer
                    </div>
                    <div style="font-size:15px;color:#1e1b4b;line-height:1.7;font-weight:500">
                        {resp['answer']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if resp.get("explanation"):
                st.markdown(f"""
                <div style="
                    background:#f9fafb;
                    border:1px solid #e5e7eb;
                    border-radius:10px;
                    padding:16px 20px;
                    margin-bottom:12px;
                ">
                    <div style="font-size:13px;font-weight:600;color:#374151;margin-bottom:6px">
                        📖 More context
                    </div>
                    <div style="font-size:14px;color:#4b5563;line-height:1.65">
                        {resp['explanation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if resp.get("analogy"):
                st.markdown(f"""
                <div style="
                    background:#fefce8;
                    border:1px solid #fde68a;
                    border-left:4px solid #f59e0b;
                    border-radius:0 10px 10px 0;
                    padding:16px 20px;
                ">
                    <div style="font-size:13px;font-weight:600;color:#b45309;margin-bottom:5px">
                        💡 Think of it like this
                    </div>
                    <div style="font-size:14px;color:#78350f;line-height:1.65">
                        {resp['analogy']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if st.session_state.messages:
            st.markdown("<div style='margin-top:28px'/>", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:14px;font-weight:600;color:#374151;margin-bottom:10px">
                Recent questions
            </div>
            """, unsafe_allow_html=True)
            for msg in reversed(st.session_state.messages[-5:]):
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

    # ─── TAB 2 · Quiz ─────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div style="margin-bottom:16px">
            <div style="font-size:20px;font-weight:700;color:#111827">Practice Quiz</div>
            <div style="font-size:14px;color:#6b7280;margin-top:3px">
                Questions adapt automatically to your current performance level.
            </div>
        </div>
        """, unsafe_allow_html=True)

        qz_c1, qz_c2 = st.columns([2, 5])
        with qz_c1:
            if st.button("Generate Quiz  →", use_container_width=True):
                st.session_state.quiz_active    = True
                st.session_state.quiz_index     = 0
                with st.spinner("Generating questions…"):
                    st.session_state.quiz_questions = quiz_gen.generate_quiz(
                        topic=selected_topic, num_questions=5,
                        class_level=session.class_level, subject=session.subject,
                    )
                st.rerun()

        if st.session_state.quiz_active and st.session_state.quiz_questions:
            q_idx = st.session_state.quiz_index
            q     = st.session_state.quiz_questions[q_idx]
            total = len(st.session_state.quiz_questions)

            # Progress strip
            pct = int(q_idx / total * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin:16px 0 20px 0">
                <div style="flex:1;background:#e5e7eb;border-radius:99px;height:6px;overflow:hidden">
                    <div style="width:{pct}%;background:linear-gradient(90deg,#4f46e5,#7c3aed);
                                height:6px;border-radius:99px;transition:width 0.4s ease"></div>
                </div>
                <span style="font-size:12px;font-weight:600;color:#6b7280;white-space:nowrap">
                    Question {q_idx+1} of {total}
                </span>
            </div>
            """, unsafe_allow_html=True)

            # Question card
            diff  = q.get("difficulty", "medium")
            qtype = q.get("type", "mcq")
            diff_map  = {"easy": ("#059669","#f0fdf4"), "medium": ("#f59e0b","#fffbeb"),
                         "hard": ("#dc2626","#fef2f2")}
            dc, db    = diff_map.get(diff, ("#6b7280","#f9fafb"))
            type_map  = {"mcq": "Multiple Choice", "short_answer": "Short Answer"}

            st.markdown(f"""
            <div style="
                background:#ffffff;
                border:1px solid #e5e7eb;
                border-radius:12px;
                padding:28px 24px;
                margin-bottom:20px;
                box-shadow:0 1px 4px rgba(0,0,0,0.06);
            ">
                <div style="display:flex;gap:8px;margin-bottom:14px">
                    <span style="background:{db};color:{dc};font-size:11px;font-weight:700;
                                 padding:3px 11px;border-radius:99px;letter-spacing:0.06em;
                                 -webkit-text-fill-color:{dc}">
                        {diff.upper()}
                    </span>
                    <span style="background:#f3f4f6;color:#374151;font-size:11px;font-weight:600;
                                 padding:3px 11px;border-radius:99px;letter-spacing:0.05em;
                                 -webkit-text-fill-color:#374151">
                        {type_map.get(qtype, qtype)}
                    </span>
                </div>
                <div style="font-size:17px;font-weight:600;color:#111827;line-height:1.6">
                    {q['question']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Answers
            if qtype == "mcq":
                opts = q.get("options", {})
                sel  = st.radio("Choose your answer:",
                                list(opts.keys()),
                                format_func=lambda x: f"{x}.   {opts[x]}",
                                label_visibility="collapsed")
                if st.button("Submit Answer", use_container_width=True, key=f"sub_{q_idx}"):
                    with st.spinner("Evaluating…"):
                        res = quiz_gen.evaluate_answer(q, sel)
                    session.record_question(q["question"], sel, res["is_correct"])
                    session.update_confidence(selected_topic, res["is_correct"])

                    if res["is_correct"]:
                        st.success(f"✅  Correct!   {res.get('feedback','')}")
                    else:
                        st.error(f"❌  {res.get('feedback','Not quite right.')}")

                    st.markdown(f"""
                    <div style="
                        background:#f9fafb;border:1px solid #e5e7eb;
                        border-radius:10px;padding:16px 20px;margin-top:12px;
                    ">
                        <div style="font-size:12px;font-weight:700;color:#6b7280;
                                    text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px">
                            Explanation
                        </div>
                        <div style="font-size:14px;color:#374151;line-height:1.65">
                            {q.get('explanation','')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if q_idx < total - 1:
                        if st.button("Next Question  →", use_container_width=True,
                                     key=f"next_{q_idx}"):
                            st.session_state.quiz_index += 1
                            st.rerun()
                    else:
                        st.balloons()
                        st.success("🎓  Quiz complete! Great work.")
            else:
                ans = st.text_area("Write your answer here:", height=110,
                                   placeholder="Type your answer…")
                if st.button("Submit Answer", use_container_width=True,
                             key=f"sub_sa_{q_idx}"):
                    with st.spinner("Evaluating…"):
                        res = quiz_gen.evaluate_answer(q, ans)
                    session.record_question(q["question"], ans, res["is_correct"])
                    session.update_confidence(selected_topic, res["is_correct"])
                    if res["is_correct"]:
                        st.success("✅  Great answer!")
                    else:
                        st.warning("Good effort — here is what we were looking for.")
                    st.info(f"**Feedback:** {res.get('feedback','')}")

    # ─── TAB 3 · Study ────────────────────────────────────────
    with tab3:
        st.markdown(f"""
        <div style="margin-bottom:16px">
            <div style="font-size:20px;font-weight:700;color:#111827">Study Notes</div>
            <div style="font-size:14px;color:#6b7280;margin-top:3px">
                AI-generated summary for <strong style="color:#4f46e5">{selected_topic}</strong>
                based on NCERT content.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Generate Study Notes  →", use_container_width=False):
            with st.spinner("Loading content…"):
                expl = explain_engine.explain_topic(
                    topic=selected_topic,
                    class_level=session.class_level,
                    subject=session.subject,
                )

            if expl.get("explanation"):
                # Title
                st.markdown(f"""
                <div style="
                    font-size:24px;font-weight:800;color:#111827;
                    margin:20px 0 12px 0;letter-spacing:-0.4px;
                ">
                    {selected_topic}
                </div>
                """, unsafe_allow_html=True)

                # Body
                st.markdown(f"""
                <div style="
                    background:#ffffff;border:1px solid #e5e7eb;
                    border-radius:12px;padding:24px;
                    font-size:15px;color:#374151;line-height:1.75;
                    box-shadow:0 1px 4px rgba(0,0,0,0.05);
                ">
                    {expl['explanation']}
                </div>
                """, unsafe_allow_html=True)

                if expl.get("analogy"):
                    st.markdown(f"""
                    <div style="
                        background:#fefce8;border:1px solid #fde68a;
                        border-left:4px solid #f59e0b;
                        border-radius:0 10px 10px 0;
                        padding:18px 22px;margin-top:16px;
                    ">
                        <div style="font-size:12px;font-weight:700;color:#b45309;
                                    text-transform:uppercase;letter-spacing:0.07em;margin-bottom:7px">
                            💡 Real-world Analogy
                        </div>
                        <div style="font-size:14px;color:#78350f;line-height:1.65">
                            {expl['analogy']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                if expl.get("example"):
                    st.markdown(f"""
                    <div style="
                        background:#f0fdf4;border:1px solid #bbf7d0;
                        border-left:4px solid #10b981;
                        border-radius:0 10px 10px 0;
                        padding:18px 22px;margin-top:12px;
                    ">
                        <div style="font-size:12px;font-weight:700;color:#065f46;
                                    text-transform:uppercase;letter-spacing:0.07em;margin-bottom:7px">
                            📌 Example
                        </div>
                        <div style="font-size:14px;color:#064e3b;line-height:1.65">
                            {expl['example']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                if expl.get("key_points"):
                    st.markdown("""
                    <div style="font-size:14px;font-weight:700;color:#111827;
                                margin:20px 0 10px 0">
                        Key points to remember
                    </div>
                    """, unsafe_allow_html=True)
                    for pt in expl["key_points"]:
                        st.markdown(f"""
                        <div style="
                            background:#ffffff;border:1px solid #e5e7eb;
                            border-radius:8px;padding:12px 16px;
                            margin-bottom:8px;font-size:14px;color:#374151;
                            display:flex;align-items:flex-start;gap:10px;
                        ">
                            <span style="color:#4f46e5;font-weight:700;flex-shrink:0">→</span>
                            <span>{pt}</span>
                        </div>
                        """, unsafe_allow_html=True)

    # ─── TAB 4 · Progress ─────────────────────────────────────
    with tab4:
        st.markdown("""
        <div style="margin-bottom:20px">
            <div style="font-size:20px;font-weight:700;color:#111827">My Progress</div>
            <div style="font-size:14px;color:#6b7280;margin-top:3px">
                Your performance overview for this session.
            </div>
        </div>
        """, unsafe_allow_html=True)

        summary = session.get_progress_summary()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Questions Answered", summary["total_questions"])
        m2.metric("Accuracy",  f"{summary['accuracy']:.1f}%")
        m3.metric("Topics Mastered",
                  len([v for v in summary["topic_confidence"].values() if v >= 0.7]))
        m4.metric("Session Duration", f"{summary['session_duration_minutes']:.0f} min")

        st.divider()

        if summary["topic_confidence"]:
            st.markdown("""
            <div style="font-size:15px;font-weight:700;color:#111827;margin-bottom:14px">
                Topic Mastery
            </div>
            """, unsafe_allow_html=True)
            for topic, conf in summary["topic_confidence"].items():
                lc, rc = st.columns([4, 1])
                with lc:
                    st.progress(conf, text=topic)
                with rc:
                    if conf >= 0.7:
                        st.markdown("<div style='color:#059669;font-size:13px;font-weight:600;"
                                    "margin-top:8px'>Strong ✓</div>", unsafe_allow_html=True)
                    elif conf >= 0.4:
                        st.markdown("<div style='color:#f59e0b;font-size:13px;font-weight:600;"
                                    "margin-top:8px'>Building</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='color:#dc2626;font-size:13px;font-weight:600;"
                                    "margin-top:8px'>Practice</div>", unsafe_allow_html=True)

        st.divider()
        sv1, sv2 = st.columns([1, 4])
        with sv1:
            if st.button("💾 Save Progress", use_container_width=True):
                os.makedirs("sessions", exist_ok=True)
                sp = f"sessions/{session.student_id}_{datetime.now():%Y%m%d_%H%M%S}.json"
                session.save_session(sp)
                st.success("Progress saved!")

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align:center;
    padding:36px 0 12px;
    font-size:13px;
    color:#9ca3af;
    border-top:1px solid #e5e7eb;
    margin-top:40px;
">
    <strong style="color:#374151">EduCore</strong>
    &nbsp;·&nbsp; Intelligent Learning for CBSE Classes 6–10
    &nbsp;·&nbsp; © 2025
</div>
""", unsafe_allow_html=True)
