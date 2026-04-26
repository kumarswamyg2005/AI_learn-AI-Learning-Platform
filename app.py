"""EduCore — Intelligent Learning Platform"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from datetime import datetime
import os

from config import CLASSES, SUBJECTS
from tutor.session import StudentSession
from tutor.quiz import QuizGenerator
from tutor.explain import ExplanationEngine
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
# COMPLETE DESIGN SYSTEM  — Dark Futuristic
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ══════════════════════════════════════════
   1. GLOBAL RESET
══════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    font-family: 'Inter', -apple-system, sans-serif !important;
    background: #080c16 !important;
    color: #e2e8f0 !important;
    -webkit-font-smoothing: antialiased;
}

/* Remove all Streamlit chrome except sidebar toggle */
#MainMenu, footer, .stDeployButton,
[data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
}
header { visibility: hidden !important; }

/* ── Sidebar collapse/expand arrow button ── */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    align-items: center !important;
    justify-content: center !important;
    width: 36px !important;
    height: 36px !important;
    background: rgba(99,102,241,0.15) !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    border-radius: 50% !important;
    color: #818cf8 !important;
    cursor: pointer !important;
    top: 14px !important;
    z-index: 9999 !important;
    box-shadow: 0 0 12px rgba(99,102,241,0.25) !important;
    transition: background 0.2s, box-shadow 0.2s !important;
}
[data-testid="collapsedControl"]:hover {
    background: rgba(99,102,241,0.30) !important;
    box-shadow: 0 0 20px rgba(99,102,241,0.45) !important;
}
[data-testid="collapsedControl"] svg {
    fill: #818cf8 !important;
    color: #818cf8 !important;
    stroke: #818cf8 !important;
}

.main .block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1300px !important;
    background: transparent !important;
}

/* ══════════════════════════════════════════
   2. SIDEBAR
══════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #0a0e1a !important;
    border-right: 1px solid rgba(99,102,241,0.15) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
    padding-top: 0 !important;
}
/* Force ALL text inside sidebar to be visible */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span:not([data-testid]),
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stMarkdown p {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}

/* Sidebar section labels (CAPS) */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #4f5a6b !important;
    -webkit-text-fill-color: #4f5a6b !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}

/* Sidebar inputs */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}
[data-testid="stSidebar"] input::placeholder {
    color: #4a5568 !important;
    -webkit-text-fill-color: #4a5568 !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* Sidebar selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #4a5568 !important;
}

/* Sidebar expander */
[data-testid="stSidebar"] details {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    overflow: hidden;
}
[data-testid="stSidebar"] details summary {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
}
[data-testid="stSidebar"] details summary svg {
    fill: #4a5568 !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    margin: 10px 0 !important;
}

/* Sidebar tab labels */
[data-testid="stSidebar"] [data-baseweb="tab"] {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] [aria-selected="true"] {
    color: #a5b4fc !important;
    -webkit-text-fill-color: #a5b4fc !important;
}

/* ══════════════════════════════════════════
   3. BUTTONS
══════════════════════════════════════════ */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: linear-gradient(135deg, #4f46e5, #6d28d9) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 9px 18px !important;
    letter-spacing: 0.01em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 20px rgba(99,102,241,0.2), 0 1px 3px rgba(0,0,0,0.3) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #5b52f0, #7c3aed) !important;
    box-shadow: 0 0 30px rgba(99,102,241,0.4), 0 4px 12px rgba(0,0,0,0.3) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
    box-shadow: 0 0 15px rgba(99,102,241,0.3) !important;
}

/* ══════════════════════════════════════════
   4. INPUTS (main content)
══════════════════════════════════════════ */
.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    padding: 11px 15px !important;
    transition: all 0.2s ease !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15), 0 0 20px rgba(99,102,241,0.08) !important;
    background: rgba(99,102,241,0.05) !important;
    outline: none !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
}
.stTextInput label, .stTextArea label {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
}

/* ══════════════════════════════════════════
   5. SELECTBOX (main)
══════════════════════════════════════════ */
.stSelectbox [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}
.stSelectbox [data-baseweb="select"] span {
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    font-size: 14px !important;
}
.stSelectbox label {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

/* ══════════════════════════════════════════
   6. TABS
══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 3px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 9px 22px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #4a5568 !important;
    -webkit-text-fill-color: #4a5568 !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    background: rgba(255,255,255,0.04) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4f46e5, #6d28d9) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    box-shadow: 0 0 20px rgba(99,102,241,0.3), 0 2px 8px rgba(0,0,0,0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding-top: 24px !important;
}

/* ══════════════════════════════════════════
   7. METRICS
══════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 20px 22px !important;
    backdrop-filter: blur(10px) !important;
}
[data-testid="stMetricLabel"] > div {
    color: #4a5568 !important;
    -webkit-text-fill-color: #4a5568 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
}
[data-testid="stMetricDelta"] svg { display: none !important; }
[data-testid="stMetricDelta"] > div {
    color: #34d399 !important;
    -webkit-text-fill-color: #34d399 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

/* ══════════════════════════════════════════
   8. ALERTS
══════════════════════════════════════════ */
.stSuccess > div {
    background: rgba(52,211,153,0.08) !important;
    border: 1px solid rgba(52,211,153,0.25) !important;
    border-radius: 10px !important;
    color: #6ee7b7 !important;
    -webkit-text-fill-color: #6ee7b7 !important;
}
.stError > div {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.25) !important;
    border-radius: 10px !important;
    color: #fca5a5 !important;
    -webkit-text-fill-color: #fca5a5 !important;
}
.stWarning > div {
    background: rgba(251,191,36,0.08) !important;
    border: 1px solid rgba(251,191,36,0.25) !important;
    border-radius: 10px !important;
    color: #fde68a !important;
    -webkit-text-fill-color: #fde68a !important;
}
.stInfo > div {
    background: rgba(99,102,241,0.08) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important;
    color: #a5b4fc !important;
    -webkit-text-fill-color: #a5b4fc !important;
}

/* ══════════════════════════════════════════
   9. PROGRESS BAR
══════════════════════════════════════════ */
.stProgress > div > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 99px !important;
    height: 6px !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6366f1, #818cf8) !important;
    border-radius: 99px !important;
    box-shadow: 0 0 10px rgba(99,102,241,0.5) !important;
}
.stProgress p {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* ══════════════════════════════════════════
   10. RADIO BUTTONS
══════════════════════════════════════════ */
.stRadio > div { gap: 8px !important; }
.stRadio label {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stRadio label:hover {
    border-color: rgba(99,102,241,0.4) !important;
    background: rgba(99,102,241,0.06) !important;
}
.stRadio label span {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* ══════════════════════════════════════════
   11. FILE UPLOADER
══════════════════════════════════════════ */
[data-testid="stFileUploader"] > div {
    background: rgba(255,255,255,0.02) !important;
    border: 2px dashed rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"]:hover > div {
    border-color: rgba(99,102,241,0.4) !important;
    background: rgba(99,102,241,0.04) !important;
}
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small {
    color: #4a5568 !important;
    -webkit-text-fill-color: #4a5568 !important;
}

/* ══════════════════════════════════════════
   12. CAPTION + MARKDOWN TEXT
══════════════════════════════════════════ */
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #4a5568 !important;
    -webkit-text-fill-color: #4a5568 !important;
    font-size: 12px !important;
}
.stMarkdown p {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    line-height: 1.7 !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    font-weight: 700 !important;
}
.stMarkdown strong {
    color: #c7d2fe !important;
    -webkit-text-fill-color: #c7d2fe !important;
}
.stMarkdown li {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}

/* ══════════════════════════════════════════
   13. DIVIDER
══════════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    margin: 18px 0 !important;
}

/* ══════════════════════════════════════════
   14. CHAT MESSAGES
══════════════════════════════════════════ */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
}
[data-testid="stChatMessage"] p {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}

/* ══════════════════════════════════════════
   15. SPINNER
══════════════════════════════════════════ */
[data-testid="stSpinner"] p {
    color: #4a5568 !important;
    -webkit-text-fill-color: #4a5568 !important;
}

/* ══════════════════════════════════════════
   16. SCROLLBAR
══════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.15); }

/* ══════════════════════════════════════════
   17. PLOTLY CHART BACKGROUND
══════════════════════════════════════════ */
.js-plotly-plot .plotly { background: transparent !important; }

/* ══════════════════════════════════════════
   18. DOWNLOAD BUTTON
══════════════════════════════════════════ */
.stDownloadButton > button {
    background: rgba(52,211,153,0.12) !important;
    border: 1px solid rgba(52,211,153,0.3) !important;
    color: #34d399 !important;
    -webkit-text-fill-color: #34d399 !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    background: rgba(52,211,153,0.2) !important;
    box-shadow: 0 0 20px rgba(52,211,153,0.2) !important;
}

/* ══════════════════════════════════════════
   19. SELECTBOX DROPDOWN OPTIONS
══════════════════════════════════════════ */
[data-baseweb="popover"] {
    background: #0d1221 !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    box-shadow: 0 24px 60px rgba(0,0,0,0.6) !important;
}
[data-baseweb="option"] {
    background: transparent !important;
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    font-size: 13px !important;
    border-radius: 6px !important;
}
[data-baseweb="option"]:hover, [aria-selected="true"][data-baseweb="option"] {
    background: rgba(99,102,241,0.15) !important;
    color: #c7d2fe !important;
    -webkit-text-fill-color: #c7d2fe !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPER: Glass card HTML
# ─────────────────────────────────────────────────────────────
def glass(content: str, pad="24px", radius="14px", glow_color=""):
    glow = f"box-shadow:0 0 40px {glow_color};" if glow_color else ""
    return f"""
    <div style="
        background:rgba(255,255,255,0.03);
        border:1px solid rgba(255,255,255,0.07);
        border-radius:{radius};
        padding:{pad};
        backdrop-filter:blur(12px);
        -webkit-backdrop-filter:blur(12px);
        {glow}
    ">{content}</div>"""


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
for k, v in {
    "student_session": None,
    "messages": [],
    "quiz_active": False,
    "quiz_questions": [],
    "quiz_index": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────
# ENGINES (cached)
# ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_engines():
    return QuizGenerator(), ExplanationEngine(), ReportGenerator(), SpeechProcessor()

quiz_gen, explain_engine, report_gen, speech_proc = load_engines()


# ═════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:24px 4px 16px">
        <div style="
            font-family:'Space Grotesk',sans-serif;
            font-size:21px;font-weight:700;
            color:#e2e8f0;letter-spacing:-0.4px;
            -webkit-text-fill-color:#e2e8f0;
        ">🎓 EduCore</div>
        <div style="
            font-size:11px;color:#64748b;font-weight:500;
            margin-top:3px;letter-spacing:0.04em;
            -webkit-text-fill-color:#64748b;
        ">INTELLIGENT LEARNING PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("STUDENT")
    student_id = st.text_input("name", value="Student", key="student_id",
                               placeholder="Your name…",
                               label_visibility="collapsed")

    st.caption("LEARNING PATH")
    selected_class   = st.selectbox("class", CLASSES,
                                    format_func=lambda x: f"Class {x}",
                                    label_visibility="collapsed")
    selected_subject = st.selectbox("subject", list(SUBJECTS.keys()),
                                    label_visibility="collapsed")
    st.divider()

    st.divider()

    if st.button("▶  Start Session", use_container_width=True, key="start_btn"):
        st.session_state.student_session = StudentSession(
            student_id=student_id,
            subject=selected_subject,
            class_level=selected_class,
        )
        st.success(f"Welcome, {student_id}!")

    # Live stats
    if st.session_state.student_session:
        sess = st.session_state.student_session
        sm   = sess.get_progress_summary()
        st.divider()
        st.caption("PERFORMANCE")
        c1, c2 = st.columns(2)
        c1.metric("Accuracy",  f"{sm['accuracy']:.0f}%")
        c2.metric("Answered",  sm["total_questions"])

        if sm["topic_confidence"]:
            tnames = list(sm["topic_confidence"].keys())
            tvals  = [sm["topic_confidence"][t] * 100 for t in tnames]
            fig = go.Figure(go.Scatterpolar(
                r=tvals, theta=tnames, fill="toself",
                line_color="#6366f1",
                fillcolor="rgba(99,102,241,0.1)",
                line_width=2,
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 100],
                                   tickfont=dict(size=7, color="#64748b"),
                                   gridcolor="rgba(255,255,255,0.05)"),
                    angularaxis=dict(tickfont=dict(size=8, color="#4a5568")),
                ),
                showlegend=False, height=190,
                margin=dict(l=16, r=16, t=16, b=16),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
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


# ═════════════════════════════════════════════════════════════
# SIDEBAR TOGGLE — uses components.html so JS actually runs
# ═════════════════════════════════════════════════════════════
components.html("""
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:transparent; overflow:hidden; }
  #menuBtn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99,102,241,0.18);
    border: 1px solid rgba(99,102,241,0.45);
    border-radius: 10px;
    padding: 8px 18px;
    color: #a5b4fc;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.03em;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 4px 18px rgba(99,102,241,0.22);
    backdrop-filter: blur(8px);
    transition: background 0.2s, box-shadow 0.2s;
    margin-top: 4px;
  }
  #menuBtn:hover {
    background: rgba(99,102,241,0.32);
    box-shadow: 0 4px 24px rgba(99,102,241,0.4);
  }
</style>
<button id="menuBtn">&#9776;&nbsp; Menu</button>
<script>
  document.getElementById('menuBtn').addEventListener('click', function() {
    var doc = window.parent.document;
    // When sidebar is collapsed the expand button has this testid
    var btn = doc.querySelector('[data-testid="collapsedControl"]');
    // When sidebar is open the collapse button is inside the sidebar
    if (!btn) btn = doc.querySelector('[data-testid="stSidebarCollapseButton"] button');
    if (!btn) btn = doc.querySelector('[data-testid="stSidebar"] button');
    if (btn) btn.click();
  });
</script>
""", height=48)

# ═════════════════════════════════════════════════════════════
# MAIN  ──  HOME
# ═════════════════════════════════════════════════════════════
if not st.session_state.student_session:

    # ── HERO ─────────────────────────────────────────────────
    st.markdown(
        '<div style="position:relative;background:linear-gradient(135deg,#0d0f1d 0%,#120e2a 40%,#0a1628 100%);border:1px solid rgba(99,102,241,0.2);border-radius:20px;padding:72px 60px 64px;margin-bottom:24px;overflow:hidden;">'
        '<div style="position:absolute;top:-120px;right:-80px;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(99,102,241,0.12) 0%,transparent 65%);pointer-events:none;"></div>'
        '<div style="position:absolute;bottom:-100px;left:30%;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle,rgba(139,92,246,0.08) 0%,transparent 65%);pointer-events:none;"></div>'
        '<div style="display:inline-flex;align-items:center;gap:6px;background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.3);border-radius:99px;padding:5px 14px 5px 10px;margin-bottom:24px;">'
        '<span style="width:6px;height:6px;border-radius:50%;background:#6366f1;box-shadow:0 0 8px #6366f1;display:inline-block;"></span>'
        '<span style="font-size:11px;font-weight:700;color:#a5b4fc;letter-spacing:0.1em;-webkit-text-fill-color:#a5b4fc;">POWERED BY GOOGLE GEMINI AI</span>'
        '</div>'
        '<h1 style="font-family:\'Space Grotesk\',sans-serif;font-size:52px;font-weight:700;line-height:1.12;letter-spacing:-1.5px;color:#f1f5f9;-webkit-text-fill-color:#f1f5f9;margin:0 0 20px;max-width:640px;">Learn Smarter.<br>'
        '<span style="color:#818cf8;-webkit-text-fill-color:#818cf8;">Grow Faster.</span></h1>'
        '<p style="font-size:17px;color:#94a3b8;max-width:520px;line-height:1.75;margin:0 0 36px;-webkit-text-fill-color:#94a3b8;">An adaptive platform built on the official CBSE curriculum for Classes 6–10. Personalised explanations, smart quizzes, and real-time progress analytics.</p>'
        '<div style="display:flex;gap:10px;flex-wrap:wrap;">'
        '<span style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#94a3b8;-webkit-text-fill-color:#94a3b8;border-radius:8px;padding:7px 16px;font-size:13px;font-weight:500;">📚 Classes 6–10</span>'
        '<span style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#94a3b8;-webkit-text-fill-color:#94a3b8;border-radius:8px;padding:7px 16px;font-size:13px;font-weight:500;">🌐 5 Languages</span>'
        '<span style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#94a3b8;-webkit-text-fill-color:#94a3b8;border-radius:8px;padding:7px 16px;font-size:13px;font-weight:500;">📊 Live Analytics</span>'
        '<span style="background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.2);color:#34d399;-webkit-text-fill-color:#34d399;border-radius:8px;padding:7px 16px;font-size:13px;font-weight:600;">✦ 100% Free</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── FEATURE CARDS ────────────────────────────────────────
    features = [
        ("🎯","#6366f1","Truly Adaptive",
         "Difficulty auto-adjusts in real-time so you're always in the right challenge zone."),
        ("🧠","#8b5cf6","AI Explanations",
         "Every concept broken down simply, with relatable real-world analogies."),
        ("📚","#06b6d4","NCERT Aligned",
         "Content sourced directly from official CBSE textbooks, nothing extra."),
        ("🌐","#10b981","5 Languages",
         "Study in English, Hindi, Telugu, Kannada, or Malayalam."),
        ("📊","#f59e0b","Progress Analytics",
         "Radar charts and mastery scores across every topic you study."),
        ("🎤","#ec4899","Voice Mode",
         "Ask questions by voice and hear explanations read back to you."),
    ]

    r1, r2 = st.columns(3), st.columns(3)
    for i, (icon, color, title, desc) in enumerate(features):
        col = (r1 if i < 3 else r2)[i % 3]
        with col:
            st.markdown(f"""
            <div style="
                background:rgba(255,255,255,0.02);
                border:1px solid rgba(255,255,255,0.06);
                border-radius:14px;
                padding:26px 22px;
                margin-bottom:14px;
                position:relative;
                overflow:hidden;
                transition:border-color 0.2s;
            ">
                <div style="
                    position:absolute;top:0;left:0;
                    width:100%;height:2px;
                    background:linear-gradient(90deg,{color},transparent);
                "></div>
                <div style="font-size:28px;margin-bottom:12px">{icon}</div>
                <div style="
                    font-size:15px;font-weight:700;
                    color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                    margin-bottom:8px;letter-spacing:-0.2px;
                ">{title}</div>
                <div style="
                    font-size:13px;color:#4a5568;
                    line-height:1.65;-webkit-text-fill-color:#4a5568;
                ">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── STATS BAR ────────────────────────────────────────────
    st.markdown(
        '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:32px 48px;margin:4px 0 28px;display:flex;justify-content:space-around;align-items:center;flex-wrap:wrap;gap:20px;">'
        '<div style="text-align:center;">'
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:38px;font-weight:700;color:#818cf8;-webkit-text-fill-color:#818cf8;letter-spacing:-1px;line-height:1;">15+</div>'
        '<div style="font-size:12px;color:#64748b;font-weight:600;margin-top:6px;letter-spacing:0.05em;-webkit-text-fill-color:#64748b;">TEXTBOOKS</div>'
        '</div>'
        '<div style="width:1px;height:40px;background:rgba(255,255,255,0.06);"></div>'
        '<div style="text-align:center;">'
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:38px;font-weight:700;color:#a78bfa;-webkit-text-fill-color:#a78bfa;letter-spacing:-1px;line-height:1;">1,500+</div>'
        '<div style="font-size:12px;color:#64748b;font-weight:600;margin-top:6px;letter-spacing:0.05em;-webkit-text-fill-color:#64748b;">QUESTIONS</div>'
        '</div>'
        '<div style="width:1px;height:40px;background:rgba(255,255,255,0.06);"></div>'
        '<div style="text-align:center;">'
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:38px;font-weight:700;color:#34d399;-webkit-text-fill-color:#34d399;letter-spacing:-1px;line-height:1;">5</div>'
        '<div style="font-size:12px;color:#64748b;font-weight:600;margin-top:6px;letter-spacing:0.05em;-webkit-text-fill-color:#64748b;">LANGUAGES</div>'
        '</div>'
        '<div style="width:1px;height:40px;background:rgba(255,255,255,0.06);"></div>'
        '<div style="text-align:center;">'
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:38px;font-weight:700;color:#f59e0b;-webkit-text-fill-color:#f59e0b;letter-spacing:-1px;line-height:1;">Free</div>'
        '<div style="font-size:12px;color:#64748b;font-weight:600;margin-top:6px;letter-spacing:0.05em;-webkit-text-fill-color:#64748b;">ALWAYS</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── HOW TO START ─────────────────────────────────────────
    st.markdown("""
    <div style="
        font-size:16px;font-weight:700;
        color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
        margin-bottom:14px;letter-spacing:-0.2px;
    ">Get started in 3 steps</div>
    """, unsafe_allow_html=True)

    steps = [
        ("#6366f1","rgba(99,102,241,0.08)","01","Fill your profile",
         "Enter your name, select your class and subject in the sidebar."),
        ("#8b5cf6","rgba(139,92,246,0.08)","02","Choose a topic",
         "Select any topic from the official CBSE curriculum."),
        ("#10b981","rgba(16,185,129,0.08)","03","Start learning",
         "Ask questions, take quizzes, and track your growth in real-time."),
    ]
    sc = st.columns(3)
    for col, (border, bg, num, heading, body) in zip(sc, steps):
        with col:
            st.markdown(f"""
            <div style="
                background:{bg};
                border:1px solid {border}30;
                border-radius:12px;
                padding:22px;
            ">
                <div style="
                    font-size:11px;font-weight:800;
                    color:{border};-webkit-text-fill-color:{border};
                    letter-spacing:0.12em;margin-bottom:10px;
                ">STEP {num}</div>
                <div style="
                    font-size:15px;font-weight:700;
                    color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                    margin-bottom:7px;
                ">{heading}</div>
                <div style="
                    font-size:13px;color:#4a5568;
                    line-height:1.6;-webkit-text-fill-color:#4a5568;
                ">{body}</div>
            </div>
            """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
# MAIN  ──  ACTIVE SESSION
# ═════════════════════════════════════════════════════════════
else:
    session = st.session_state.student_session
    summary = session.get_progress_summary()
    lvl     = session.get_current_level()
    lvl_color = {"easy":"#34d399","medium":"#f59e0b","hard":"#f87171"}.get(lvl,"#a5b4fc")

    # ── SESSION HEADER ────────────────────────────────────────
    st.markdown(f"""
    <div style="
        background:rgba(255,255,255,0.02);
        border:1px solid rgba(255,255,255,0.07);
        border-radius:14px;
        padding:20px 28px;
        display:flex;align-items:center;
        justify-content:space-between;
        margin-bottom:20px;
        flex-wrap:wrap;gap:16px;
    ">
        <div>
            <div style="
                font-size:11px;font-weight:700;color:#64748b;
                text-transform:uppercase;letter-spacing:0.1em;
                margin-bottom:5px;-webkit-text-fill-color:#64748b;
            ">Active Session</div>
            <div style="
                font-family:'Space Grotesk',sans-serif;
                font-size:20px;font-weight:700;
                color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                letter-spacing:-0.3px;
            ">{session.subject}&nbsp;&nbsp;·&nbsp;&nbsp;Class {session.class_level}</div>
        </div>
        <div style="display:flex;gap:32px;text-align:center">
            <div>
                <div style="
                    font-size:22px;font-weight:800;
                    color:#818cf8;-webkit-text-fill-color:#818cf8;
                    letter-spacing:-0.5px;line-height:1;
                ">{summary['accuracy']:.0f}%</div>
                <div style="
                    font-size:10px;color:#64748b;font-weight:600;
                    margin-top:4px;letter-spacing:0.08em;
                    -webkit-text-fill-color:#64748b;text-transform:uppercase;
                ">Accuracy</div>
            </div>
            <div>
                <div style="
                    font-size:22px;font-weight:800;
                    color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                    letter-spacing:-0.5px;line-height:1;
                ">{summary['total_questions']}</div>
                <div style="
                    font-size:10px;color:#64748b;font-weight:600;
                    margin-top:4px;letter-spacing:0.08em;
                    -webkit-text-fill-color:#64748b;text-transform:uppercase;
                ">Answered</div>
            </div>
            <div>
                <div style="
                    font-size:22px;font-weight:800;
                    color:{lvl_color};-webkit-text-fill-color:{lvl_color};
                    letter-spacing:-0.5px;line-height:1;
                ">{lvl.upper()}</div>
                <div style="
                    font-size:10px;color:#64748b;font-weight:600;
                    margin-top:4px;letter-spacing:0.08em;
                    -webkit-text-fill-color:#64748b;text-transform:uppercase;
                ">Level</div>
            </div>
            <div>
                <div style="
                    font-size:22px;font-weight:800;
                    color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                    letter-spacing:-0.5px;line-height:1;
                ">{summary['session_duration_minutes']:.0f}m</div>
                <div style="
                    font-size:10px;color:#64748b;font-weight:600;
                    margin-top:4px;letter-spacing:0.08em;
                    -webkit-text-fill-color:#64748b;text-transform:uppercase;
                ">Session</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Topic selector
    topics = SUBJECTS.get(session.subject, [])
    tc1, tc2 = st.columns([5, 1])
    with tc1:
        selected_topic = st.selectbox("Topic", topics, key="topic")
    with tc2:
        st.markdown("<div style='height:28px'/>", unsafe_allow_html=True)
        if st.button("↺", use_container_width=True):
            st.rerun()
    if selected_topic:
        session.set_topic(selected_topic)

    st.markdown("<div style='height:6px'/>", unsafe_allow_html=True)

    # ── TABS ──────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬  Ask Anything",
        "📝  Practice Quiz",
        "📖  Study Notes",
        "📊  My Progress",
    ])

    # ─── ASK ─────────────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div style="margin-bottom:20px">
            <div style="
                font-size:20px;font-weight:700;
                color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                letter-spacing:-0.3px;margin-bottom:4px;
            ">Ask Anything</div>
            <div style="font-size:13px;color:#64748b;-webkit-text-fill-color:#64748b">
                Get a clear, simple answer to any question about this topic.
            </div>
        </div>
        """, unsafe_allow_html=True)

        qc, bc = st.columns([5, 1])
        with qc:
            user_q = st.text_input(
                "q", label_visibility="collapsed",
                placeholder=f"e.g.  What is {selected_topic}? Explain with an example.",
                key="question_input",
            )
        with bc:
            st.markdown("<div style='height:4px'/>", unsafe_allow_html=True)
            ask_btn = st.button("Ask →", use_container_width=True)

        if ask_btn and user_q:
            with st.spinner("Thinking…"):
                resp = explain_engine.answer_question(
                    question=user_q, subject=session.subject,
                    class_level=session.class_level,
                )
            st.session_state.messages.append({"role": "user", "content": user_q})

            if resp.get("answer"):
                st.markdown(f"""
                <div style="
                    background:rgba(99,102,241,0.07);
                    border:1px solid rgba(99,102,241,0.2);
                    border-left:3px solid #6366f1;
                    border-radius:0 12px 12px 0;
                    padding:20px 24px;margin:16px 0 12px;
                ">
                    <div style="
                        font-size:10px;font-weight:700;color:#6366f1;
                        -webkit-text-fill-color:#6366f1;
                        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;
                    ">Answer</div>
                    <div style="
                        font-size:15px;color:#c7d2fe;line-height:1.75;
                        -webkit-text-fill-color:#c7d2fe;font-weight:400;
                    ">{resp['answer']}</div>
                </div>
                """, unsafe_allow_html=True)

            if resp.get("explanation"):
                st.markdown(f"""
                <div style="
                    background:rgba(255,255,255,0.02);
                    border:1px solid rgba(255,255,255,0.07);
                    border-radius:12px;padding:18px 22px;margin-bottom:10px;
                ">
                    <div style="
                        font-size:10px;font-weight:700;color:#64748b;
                        -webkit-text-fill-color:#64748b;
                        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;
                    ">📖 More context</div>
                    <div style="
                        font-size:14px;color:#64748b;line-height:1.7;
                        -webkit-text-fill-color:#64748b;
                    ">{resp['explanation']}</div>
                </div>
                """, unsafe_allow_html=True)

            if resp.get("analogy"):
                st.markdown(f"""
                <div style="
                    background:rgba(245,158,11,0.06);
                    border:1px solid rgba(245,158,11,0.18);
                    border-left:3px solid #f59e0b;
                    border-radius:0 12px 12px 0;padding:18px 22px;
                ">
                    <div style="
                        font-size:10px;font-weight:700;color:#f59e0b;
                        -webkit-text-fill-color:#f59e0b;
                        letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;
                    ">💡 Think of it like this</div>
                    <div style="
                        font-size:14px;color:#fde68a;line-height:1.7;
                        -webkit-text-fill-color:#fde68a;
                    ">{resp['analogy']}</div>
                </div>
                """, unsafe_allow_html=True)

        if st.session_state.messages:
            st.markdown("<div style='height:24px'/>", unsafe_allow_html=True)
            st.markdown("""
            <div style="
                font-size:13px;font-weight:600;color:#64748b;
                -webkit-text-fill-color:#64748b;margin-bottom:10px;
            ">Recent questions</div>
            """, unsafe_allow_html=True)
            for msg in reversed(st.session_state.messages[-5:]):
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

    # ─── QUIZ ────────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div style="margin-bottom:20px">
            <div style="
                font-size:20px;font-weight:700;
                color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                letter-spacing:-0.3px;margin-bottom:4px;
            ">Practice Quiz</div>
            <div style="font-size:13px;color:#64748b;-webkit-text-fill-color:#64748b">
                Questions adapt automatically to your current performance level.
            </div>
        </div>
        """, unsafe_allow_html=True)

        gc1, gc2 = st.columns([2, 5])
        with gc1:
            if st.button("Generate Quiz →", use_container_width=True):
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
            pct   = int(q_idx / total * 100)

            # Progress strip
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:14px;margin:20px 0">
                <div style="
                    flex:1;background:rgba(255,255,255,0.05);
                    border-radius:99px;height:4px;overflow:hidden;
                ">
                    <div style="
                        width:{pct}%;
                        background:linear-gradient(90deg,#6366f1,#818cf8);
                        height:4px;border-radius:99px;
                        box-shadow:0 0 8px rgba(99,102,241,0.6);
                    "></div>
                </div>
                <span style="
                    font-size:12px;font-weight:600;
                    color:#64748b;-webkit-text-fill-color:#64748b;
                    white-space:nowrap;
                ">{q_idx+1} / {total}</span>
            </div>
            """, unsafe_allow_html=True)

            diff      = q.get("difficulty","medium")
            qtype     = q.get("type","mcq")
            diff_cfg  = {
                "easy":   ("#34d399","rgba(52,211,153,0.1)"),
                "medium": ("#f59e0b","rgba(245,158,11,0.1)"),
                "hard":   ("#f87171","rgba(248,113,113,0.1)"),
            }
            dc, db = diff_cfg.get(diff, ("#94a3b8","rgba(148,163,184,0.1)"))

            # Question card
            st.markdown(f"""
            <div style="
                background:rgba(255,255,255,0.02);
                border:1px solid rgba(255,255,255,0.07);
                border-radius:14px;padding:28px 26px;margin-bottom:20px;
            ">
                <div style="display:flex;gap:8px;margin-bottom:16px">
                    <span style="
                        background:{db};color:{dc};
                        -webkit-text-fill-color:{dc};
                        font-size:10px;font-weight:700;
                        padding:3px 11px;border-radius:99px;
                        letter-spacing:0.08em;text-transform:uppercase;
                        border:1px solid {dc}40;
                    ">{diff}</span>
                    <span style="
                        background:rgba(255,255,255,0.04);
                        color:#64748b;-webkit-text-fill-color:#64748b;
                        font-size:10px;font-weight:600;
                        padding:3px 11px;border-radius:99px;
                        letter-spacing:0.06em;text-transform:uppercase;
                        border:1px solid rgba(255,255,255,0.06);
                    ">{'Multiple Choice' if qtype=='mcq' else 'Short Answer'}</span>
                </div>
                <div style="
                    font-size:17px;font-weight:600;
                    color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                    line-height:1.6;
                ">{q['question']}</div>
            </div>
            """, unsafe_allow_html=True)

            if qtype == "mcq":
                opts = q.get("options", {})
                sel  = st.radio("ans", list(opts.keys()),
                                format_func=lambda x: f"{x}.  {opts[x]}",
                                label_visibility="collapsed")
                if st.button("Submit Answer", use_container_width=True,
                             key=f"sub_{q_idx}"):
                    with st.spinner("Evaluating…"):
                        res = quiz_gen.evaluate_answer(q, sel)
                    session.record_question(q["question"], sel, res["is_correct"])
                    session.update_confidence(selected_topic, res["is_correct"])

                    if res["is_correct"]:
                        st.success(f"✅  Correct!  {res.get('feedback','')}")
                    else:
                        st.error(f"❌  {res.get('feedback','Not quite.')}")

                    st.markdown(f"""
                    <div style="
                        background:rgba(255,255,255,0.02);
                        border:1px solid rgba(255,255,255,0.07);
                        border-radius:10px;padding:16px 20px;margin-top:12px;
                    ">
                        <div style="
                            font-size:10px;font-weight:700;color:#64748b;
                            -webkit-text-fill-color:#64748b;
                            text-transform:uppercase;letter-spacing:0.1em;margin-bottom:7px;
                        ">Explanation</div>
                        <div style="
                            font-size:14px;color:#64748b;line-height:1.65;
                            -webkit-text-fill-color:#64748b;
                        ">{q.get('explanation','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if q_idx < total - 1:
                        if st.button("Next →", use_container_width=True,
                                     key=f"next_{q_idx}"):
                            st.session_state.quiz_index += 1
                            st.rerun()
                    else:
                        st.balloons()
                        st.success("🎓  Quiz complete!")
            else:
                ans = st.text_area("ans", height=110,
                                   placeholder="Write your answer here…",
                                   label_visibility="collapsed")
                if st.button("Submit Answer", use_container_width=True,
                             key=f"sub_sa_{q_idx}"):
                    with st.spinner("Evaluating…"):
                        res = quiz_gen.evaluate_answer(q, ans)
                    session.record_question(q["question"], ans, res["is_correct"])
                    session.update_confidence(selected_topic, res["is_correct"])
                    if res["is_correct"]:
                        st.success("✅  Great answer!")
                    else:
                        st.warning("Good effort!")
                    st.info(f"**Feedback:** {res.get('feedback','')}")

    # ─── STUDY ───────────────────────────────────────────────
    with tab3:
        st.markdown(f"""
        <div style="margin-bottom:20px">
            <div style="
                font-size:20px;font-weight:700;
                color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                letter-spacing:-0.3px;margin-bottom:4px;
            ">Study Notes</div>
            <div style="font-size:13px;color:#64748b;-webkit-text-fill-color:#64748b">
                AI-generated notes for
                <span style="color:#818cf8;-webkit-text-fill-color:#818cf8;font-weight:600">
                    {selected_topic}
                </span>
                based on NCERT content.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Generate Notes →", use_container_width=False):
            with st.spinner("Loading content…"):
                expl = explain_engine.explain_topic(
                    topic=selected_topic,
                    class_level=session.class_level,
                    subject=session.subject,
                )

            if expl.get("explanation"):
                st.markdown(f"""
                <div style="
                    font-family:'Space Grotesk',sans-serif;
                    font-size:26px;font-weight:700;
                    color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                    letter-spacing:-0.5px;margin:20px 0 14px;
                ">{selected_topic}</div>

                <div style="
                    background:rgba(255,255,255,0.02);
                    border:1px solid rgba(255,255,255,0.07);
                    border-radius:14px;padding:26px;
                    font-size:15px;color:#94a3b8;line-height:1.8;
                    -webkit-text-fill-color:#94a3b8;
                ">{expl['explanation']}</div>
                """, unsafe_allow_html=True)

                if expl.get("analogy"):
                    st.markdown(f"""
                    <div style="
                        background:rgba(245,158,11,0.05);
                        border:1px solid rgba(245,158,11,0.15);
                        border-left:3px solid #f59e0b;
                        border-radius:0 12px 12px 0;
                        padding:18px 22px;margin-top:16px;
                    ">
                        <div style="
                            font-size:10px;font-weight:700;color:#f59e0b;
                            -webkit-text-fill-color:#f59e0b;
                            letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;
                        ">💡 Real-world Analogy</div>
                        <div style="
                            font-size:14px;color:#fde68a;line-height:1.7;
                            -webkit-text-fill-color:#fde68a;
                        ">{expl['analogy']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                if expl.get("example"):
                    st.markdown(f"""
                    <div style="
                        background:rgba(16,185,129,0.05);
                        border:1px solid rgba(16,185,129,0.15);
                        border-left:3px solid #10b981;
                        border-radius:0 12px 12px 0;
                        padding:18px 22px;margin-top:12px;
                    ">
                        <div style="
                            font-size:10px;font-weight:700;color:#10b981;
                            -webkit-text-fill-color:#10b981;
                            letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;
                        ">📌 Example</div>
                        <div style="
                            font-size:14px;color:#6ee7b7;line-height:1.7;
                            -webkit-text-fill-color:#6ee7b7;
                        ">{expl['example']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                if expl.get("key_points"):
                    st.markdown("""
                    <div style="
                        font-size:14px;font-weight:700;
                        color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                        margin:22px 0 12px;
                    ">Key points</div>
                    """, unsafe_allow_html=True)
                    for pt in expl["key_points"]:
                        st.markdown(f"""
                        <div style="
                            background:rgba(255,255,255,0.02);
                            border:1px solid rgba(255,255,255,0.06);
                            border-radius:8px;padding:12px 16px;
                            margin-bottom:7px;
                            display:flex;align-items:flex-start;gap:12px;
                        ">
                            <span style="
                                color:#6366f1;-webkit-text-fill-color:#6366f1;
                                font-weight:700;font-size:14px;flex-shrink:0;margin-top:1px;
                            ">→</span>
                            <span style="
                                font-size:14px;color:#94a3b8;line-height:1.6;
                                -webkit-text-fill-color:#94a3b8;
                            ">{pt}</span>
                        </div>
                        """, unsafe_allow_html=True)

    # ─── PROGRESS ────────────────────────────────────────────
    with tab4:
        st.markdown("""
        <div style="margin-bottom:20px">
            <div style="
                font-size:20px;font-weight:700;
                color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                letter-spacing:-0.3px;margin-bottom:4px;
            ">My Progress</div>
            <div style="font-size:13px;color:#64748b;-webkit-text-fill-color:#64748b">
                Performance overview for this session.
            </div>
        </div>
        """, unsafe_allow_html=True)

        summary = session.get_progress_summary()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Questions",        summary["total_questions"])
        m2.metric("Accuracy",         f"{summary['accuracy']:.1f}%")
        m3.metric("Topics Mastered",
                  len([v for v in summary["topic_confidence"].values() if v >= 0.7]))
        m4.metric("Session",          f"{summary['session_duration_minutes']:.0f} min")

        st.divider()

        if summary["topic_confidence"]:
            st.markdown("""
            <div style="
                font-size:14px;font-weight:700;
                color:#e2e8f0;-webkit-text-fill-color:#e2e8f0;
                margin-bottom:14px;
            ">Topic Mastery</div>
            """, unsafe_allow_html=True)
            for topic, conf in summary["topic_confidence"].items():
                lc, rc = st.columns([4, 1])
                with lc:
                    st.progress(conf, text=topic)
                with rc:
                    if conf >= 0.7:
                        st.markdown("""<div style='color:#34d399;-webkit-text-fill-color:#34d399;
                            font-size:12px;font-weight:600;margin-top:8px'>Strong</div>""",
                            unsafe_allow_html=True)
                    elif conf >= 0.4:
                        st.markdown("""<div style='color:#f59e0b;-webkit-text-fill-color:#f59e0b;
                            font-size:12px;font-weight:600;margin-top:8px'>Building</div>""",
                            unsafe_allow_html=True)
                    else:
                        st.markdown("""<div style='color:#f87171;-webkit-text-fill-color:#f87171;
                            font-size:12px;font-weight:600;margin-top:8px'>Practice</div>""",
                            unsafe_allow_html=True)

        st.divider()
        sv1, _ = st.columns([1, 4])
        with sv1:
            if st.button("💾 Save Progress", use_container_width=True):
                os.makedirs("sessions", exist_ok=True)
                sp = f"sessions/{session.student_id}_{datetime.now():%Y%m%d_%H%M%S}.json"
                session.save_session(sp)
                st.success("Saved!")

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align:center;padding:40px 0 16px;
    border-top:1px solid rgba(255,255,255,0.05);
    margin-top:48px;
">
    <span style="
        font-size:13px;color:#1f2937;
        -webkit-text-fill-color:#1f2937;
    ">
        <strong style="color:#64748b;-webkit-text-fill-color:#64748b">EduCore</strong>
        &nbsp;·&nbsp; Intelligent Learning for CBSE Classes 6–10 &nbsp;·&nbsp; © 2025
    </span>
</div>
""", unsafe_allow_html=True)
