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

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EduCore",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Global CSS  (injected once at the top)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label {
    color: #94a3b8 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stSidebar"] hr {
    border-color: #1e293b !important;
}

/* ── buttons ── */
.stButton > button {
    background: #4f46e5;
    color: #fff !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 20px;
    transition: background 0.2s, transform 0.15s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
}
.stButton > button:hover {
    background: #4338ca;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(79,70,229,0.35);
}
.stButton > button:active { transform: translateY(0); }

/* ── inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    border-radius: 8px !important;
    border: 1.5px solid #e2e8f0 !important;
    font-size: 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
}

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f1f5f9;
    padding: 4px;
    border-radius: 10px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    font-size: 14px;
    color: #64748b;
    background: transparent;
    border: none;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #4f46e5 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

/* ── metrics ── */
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #1e293b !important;
}
[data-testid="stMetricLabel"] {
    font-size: 12px !important;
    color: #64748b !important;
    font-weight: 500 !important;
}

/* ── alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: none !important;
}

/* ── progress ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    border-radius: 99px;
}

/* ── scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────
for key, val in {
    "student_session": None,
    "messages": [],
    "quiz_active": False,
    "quiz_questions": [],
    "quiz_index": 0,
    "quiz_submitted": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────────
# Engine Init (cached)
# ─────────────────────────────────────────────
@st.cache_resource
def load_engines():
    return QuizGenerator(), ExplanationEngine(), ReportGenerator(), SpeechProcessor()

quiz_gen, explain_engine, report_gen, speech_proc = load_engines()

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    # Logo / brand
    st.markdown("""
    <div style='padding:16px 0 8px 0'>
        <span style='font-size:22px;font-weight:800;color:#e2e8f0;letter-spacing:-0.5px'>🎓 EduCore</span><br>
        <span style='font-size:11px;color:#64748b;font-weight:500'>Intelligent Learning Platform</span>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Profile
    st.caption("STUDENT PROFILE")
    student_id = st.text_input("Your Name", value="Student", key="student_id",
                               label_visibility="collapsed",
                               placeholder="Enter your name…")
    st.caption("LEARNING PATH")
    selected_class = st.selectbox("Class", CLASSES,
                                  format_func=lambda x: f"Class {x}",
                                  label_visibility="collapsed")
    selected_subject = st.selectbox("Subject", list(SUBJECTS.keys()),
                                    label_visibility="collapsed")

    st.divider()

    # Study Materials
    st.caption("STUDY MATERIALS")
    with st.expander("📄 Upload / Download Books"):
        up_tab, dl_tab = st.tabs(["Upload PDF", "NCERT Books"])

        with up_tab:
            uploaded = st.file_uploader("Drop a PDF here", type="pdf",
                                        label_visibility="collapsed")
            if uploaded:
                dest = f"data/custom_pdfs/{uploaded.name}"
                os.makedirs("data/custom_pdfs", exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(uploaded.getbuffer())
                st.success(f"Saved — {uploaded.name}")
                if st.button("Index PDF", use_container_width=True):
                    with st.spinner("Processing…"):
                        try:
                            from rag.loader import PDFLoader
                            PDFLoader().load_pdf(dest, subject=selected_subject,
                                                 class_level=selected_class)
                            st.success("Indexed successfully!")
                        except Exception as e:
                            st.error(str(e))

        with dl_tab:
            st.caption("Download official NCERT books (Classes 6–10)")
            if st.button("Download All Books", use_container_width=True):
                with st.spinner("Downloading from ncert.nic.in…"):
                    try:
                        from download_ncert_books import download_ncert_books
                        ok, fail = download_ncert_books(verbose=False)
                        st.success(f"{ok} books downloaded!")
                        if fail:
                            st.warning(f"{fail} failed")
                    except Exception as e:
                        st.error(str(e))
            # list available
            try:
                from download_ncert_books import get_available_books
                books = get_available_books()
                for name, meta in books.items():
                    st.caption(f"✓ {name} ({meta['size_mb']} MB)")
                if not books:
                    st.caption("No books yet.")
            except Exception:
                pass

    st.divider()

    # Start session
    if st.button("▶  Start Session", use_container_width=True, key="start_btn"):
        st.session_state.student_session = StudentSession(
            student_id=student_id,
            subject=selected_subject,
            class_level=selected_class,
        )
        st.success(f"Welcome, {student_id}!")

    # Live stats (only when session active)
    if st.session_state.student_session:
        sess = st.session_state.student_session
        summary = sess.get_progress_summary()
        st.divider()
        st.caption("PERFORMANCE")
        c1, c2 = st.columns(2)
        c1.metric("Accuracy", f"{summary['accuracy']:.0f}%")
        c2.metric("Answered", summary["total_questions"])

        if summary["topic_confidence"]:
            topics = list(summary["topic_confidence"].keys())
            vals   = [summary["topic_confidence"][t] * 100 for t in topics]
            fig = go.Figure(go.Scatterpolar(
                r=vals, theta=topics, fill="toself",
                line_color="#4f46e5",
                fillcolor="rgba(79,70,229,0.15)",
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0,100],
                           tickfont=dict(size=8), gridcolor="#e2e8f0")),
                showlegend=False, height=220,
                margin=dict(l=30,r=30,t=30,b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8", size=9),
            )
            st.plotly_chart(fig, use_container_width=True,
                            config={"displayModeBar": False})

    st.divider()
    # Report
    if st.session_state.student_session:
        if st.button("⬇  Download Report", use_container_width=True):
            os.makedirs("reports", exist_ok=True)
            rpath = f"reports/{st.session_state.student_session.student_id}_report.pdf"
            if report_gen.generate_weekly_report(st.session_state.student_session, rpath):
                with open(rpath, "rb") as f:
                    st.download_button("Save PDF", f.read(),
                                       file_name=os.path.basename(rpath),
                                       mime="application/pdf",
                                       use_container_width=True)
    st.divider()
    st.caption("EduCore v2.0 · © 2025")

# ─────────────────────────────────────────────
# Main Content
# ─────────────────────────────────────────────

if not st.session_state.student_session:
    # ──────────────── HERO ────────────────
    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#4f46e5 0%,#7c3aed 60%,#a21caf 100%);
        border-radius: 16px;
        padding: 56px 48px;
        color: white;
        margin-bottom: 32px;
    ">
        <div style="max-width:600px">
            <div style="
                display:inline-block;
                background:rgba(255,255,255,0.15);
                border:1px solid rgba(255,255,255,0.25);
                border-radius:99px;
                padding:4px 14px;
                font-size:12px;
                font-weight:600;
                margin-bottom:18px;
                letter-spacing:0.06em;
            ">✦ POWERED BY GEMINI AI</div>
            <h1 style="
                font-size:44px;
                font-weight:800;
                margin:0 0 16px 0;
                line-height:1.15;
                color:white;
            ">Learn Smarter.<br>Grow Faster.</h1>
            <p style="
                font-size:17px;
                color:rgba(255,255,255,0.85);
                margin:0;
                line-height:1.65;
            ">An adaptive platform built on the official CBSE curriculum for Classes 6–10.
            Personalised explanations, instant quizzes, and detailed progress tracking —
            all in one place.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ──────────────── FEATURE CARDS ────────────────
    cards = [
        ("🎯", "Truly Adaptive", "Questions and difficulty adjust in real-time based on how you perform."),
        ("🧠", "AI Explanations", "Every topic explained simply with real-world analogies."),
        ("📚", "NCERT Aligned", "Content sourced directly from official CBSE textbooks."),
        ("🌐", "5 Languages", "Study in English, Hindi, Telugu, Kannada, or Malayalam."),
        ("📊", "Progress Analytics", "Visual dashboards to track mastery across every topic."),
        ("🎤", "Voice Mode", "Ask questions by voice and hear answers read aloud."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="
                background:white;
                border:1px solid #e2e8f0;
                border-radius:12px;
                padding:24px 20px;
                margin-bottom:16px;
                height:160px;
            ">
                <div style="font-size:28px;margin-bottom:10px">{icon}</div>
                <div style="font-size:15px;font-weight:700;color:#1e293b;margin-bottom:6px">{title}</div>
                <div style="font-size:13px;color:#64748b;line-height:1.55">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ──────────────── STATS BAR ────────────────
    st.markdown("""
    <div style="
        background:#f8fafc;
        border:1px solid #e2e8f0;
        border-radius:12px;
        padding:28px 32px;
        display:flex;
        justify-content:space-around;
        text-align:center;
        margin:8px 0 32px 0;
        flex-wrap:wrap;
        gap:16px;
    ">
        <div>
            <div style="font-size:30px;font-weight:800;color:#4f46e5">15+</div>
            <div style="font-size:13px;color:#64748b;margin-top:2px">Official Textbooks</div>
        </div>
        <div>
            <div style="font-size:30px;font-weight:800;color:#7c3aed">1,500+</div>
            <div style="font-size:13px;color:#64748b;margin-top:2px">Practice Questions</div>
        </div>
        <div>
            <div style="font-size:30px;font-weight:800;color:#a21caf">5</div>
            <div style="font-size:13px;color:#64748b;margin-top:2px">Languages</div>
        </div>
        <div>
            <div style="font-size:30px;font-weight:800;color:#0ea5e9">Free</div>
            <div style="font-size:13px;color:#64748b;margin-top:2px">Always</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ──────────────── GET STARTED ────────────────
    st.markdown("### How to get started")
    s1, s2, s3 = st.columns(3)
    for col, num, color, bg, heading, body in [
        (s1, "01", "#10b981", "#ecfdf5", "Fill your profile", "Enter your name, class and subject in the sidebar."),
        (s2, "02", "#4f46e5", "#eef2ff", "Pick a topic",      "Select any topic from the CBSE curriculum."),
        (s3, "03", "#f59e0b", "#fffbeb", "Start learning",    "Ask questions, take quizzes, and track your growth."),
    ]:
        with col:
            st.markdown(f"""
            <div style="
                background:{bg};
                border-radius:12px;
                padding:24px;
                border-left:4px solid {color};
            ">
                <div style="font-size:11px;font-weight:700;color:{color};letter-spacing:0.08em;margin-bottom:8px">STEP {num}</div>
                <div style="font-size:16px;font-weight:700;color:#1e293b;margin-bottom:6px">{heading}</div>
                <div style="font-size:13px;color:#475569;line-height:1.55">{body}</div>
            </div>
            """, unsafe_allow_html=True)

else:
    # ─────────────────────────────────────────────
    # Active Learning Session
    # ─────────────────────────────────────────────
    session = st.session_state.student_session
    summary = session.get_progress_summary()

    # Session header bar
    st.markdown(f"""
    <div style="
        background:white;
        border:1px solid #e2e8f0;
        border-radius:12px;
        padding:16px 24px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:20px;
    ">
        <div>
            <span style="font-size:13px;color:#64748b;font-weight:500">Learning Session</span><br>
            <span style="font-size:20px;font-weight:700;color:#1e293b">
                {session.subject} · Class {session.class_level}
            </span>
        </div>
        <div style="display:flex;gap:24px;text-align:center">
            <div>
                <div style="font-size:20px;font-weight:700;color:#4f46e5">{summary['accuracy']:.0f}%</div>
                <div style="font-size:11px;color:#94a3b8">Accuracy</div>
            </div>
            <div>
                <div style="font-size:20px;font-weight:700;color:#1e293b">{summary['total_questions']}</div>
                <div style="font-size:11px;color:#94a3b8">Answered</div>
            </div>
            <div>
                <div style="font-size:20px;font-weight:700;color:#10b981">{session.get_current_level().upper()}</div>
                <div style="font-size:11px;color:#94a3b8">Level</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Topic selector
    topics = SUBJECTS.get(session.subject, [])
    tc1, tc2 = st.columns([4, 1])
    with tc1:
        selected_topic = st.selectbox("Topic", topics, key="topic",
                                      label_visibility="collapsed")
    with tc2:
        if st.button("↺ Refresh", use_container_width=True):
            st.rerun()

    if selected_topic:
        session.set_topic(selected_topic)

    st.divider()

    # ── Tabs ──
    tab1, tab2, tab3, tab4 = st.tabs(["💬  Ask", "📝  Quiz", "📖  Study", "📊  Progress"])

    # ───── TAB 1 · Ask ─────
    with tab1:
        st.markdown("#### Ask anything about this topic")

        q_col, btn_col = st.columns([5, 1])
        with q_col:
            user_q = st.text_input("question", placeholder=f"e.g. Explain {selected_topic} with an example…",
                                   label_visibility="collapsed")
        with btn_col:
            st.markdown("<div style='margin-top:4px'/>", unsafe_allow_html=True)
            ask = st.button("Ask →", use_container_width=True)

        if ask and user_q:
            with st.spinner("Thinking…"):
                resp = explain_engine.answer_question(
                    question=user_q, subject=session.subject,
                    class_level=session.class_level)
            st.session_state.messages.append({"role": "user", "content": user_q})

            if resp.get("answer"):
                st.markdown(f"""
                <div style="background:#eef2ff;border-left:4px solid #4f46e5;
                            border-radius:0 10px 10px 0;padding:18px 20px;margin-top:16px">
                    <div style="font-size:12px;font-weight:600;color:#4f46e5;
                                margin-bottom:8px;text-transform:uppercase;letter-spacing:0.05em">Answer</div>
                    <div style="font-size:15px;color:#1e293b;line-height:1.65">{resp['answer']}</div>
                </div>
                """, unsafe_allow_html=True)

            if resp.get("explanation"):
                st.info(resp["explanation"])
            if resp.get("analogy"):
                st.success(f"💡 **Analogy:** {resp['analogy']}")

        if st.session_state.messages:
            st.markdown("---")
            st.markdown("#### Recent questions")
            for msg in reversed(st.session_state.messages[-6:]):
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

    # ───── TAB 2 · Quiz ─────
    with tab2:
        st.markdown("#### Practice Quiz")
        st.caption("Questions adapt to your current performance level.")

        qc1, qc2, qc3 = st.columns([2, 2, 3])
        with qc1:
            if st.button("Generate 5 Questions", use_container_width=True):
                st.session_state.quiz_active   = True
                st.session_state.quiz_index    = 0
                st.session_state.quiz_submitted = False
                with st.spinner("Generating…"):
                    st.session_state.quiz_questions = quiz_gen.generate_quiz(
                        topic=selected_topic, num_questions=5,
                        class_level=session.class_level, subject=session.subject)
                st.rerun()

        if st.session_state.quiz_active and st.session_state.quiz_questions:
            q_idx = st.session_state.quiz_index
            q     = st.session_state.quiz_questions[q_idx]
            total = len(st.session_state.quiz_questions)

            # progress strip
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin:16px 0">
                <div style="flex:1;background:#e2e8f0;border-radius:99px;height:6px">
                    <div style="width:{int((q_idx/total)*100)}%;background:#4f46e5;
                                border-radius:99px;height:6px;transition:width 0.4s"></div>
                </div>
                <span style="font-size:12px;color:#64748b;white-space:nowrap">
                    {q_idx+1} / {total}
                </span>
            </div>
            """, unsafe_allow_html=True)

            # question card
            diff_color = {"easy":"#10b981","medium":"#f59e0b","hard":"#ef4444"}.get(q.get("difficulty","medium"),"#64748b")
            st.markdown(f"""
            <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;
                        padding:24px;margin-bottom:16px">
                <div style="display:flex;gap:8px;margin-bottom:12px">
                    <span style="background:{diff_color}20;color:{diff_color};
                                 font-size:11px;font-weight:700;padding:3px 10px;
                                 border-radius:99px;text-transform:uppercase">{q.get('difficulty','')}</span>
                    <span style="background:#f1f5f9;color:#64748b;
                                 font-size:11px;font-weight:600;padding:3px 10px;
                                 border-radius:99px;text-transform:uppercase">{q.get('type','')}</span>
                </div>
                <div style="font-size:17px;font-weight:600;color:#1e293b;line-height:1.55">
                    {q['question']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # answer
            if q.get("type") == "mcq":
                opts = q.get("options", {})
                sel  = st.radio("Choose:", list(opts.keys()),
                                format_func=lambda x: f"{x}.  {opts[x]}",
                                label_visibility="collapsed")

                if st.button("Submit Answer", use_container_width=True, key=f"sub_{q_idx}"):
                    with st.spinner("Evaluating…"):
                        res = quiz_gen.evaluate_answer(q, sel)
                    session.record_question(q["question"], sel, res["is_correct"])
                    session.update_confidence(selected_topic, res["is_correct"])

                    if res["is_correct"]:
                        st.success(f"✅ Correct!  {res.get('feedback','')}")
                    else:
                        st.error(f"❌ Not quite.  {res.get('feedback','')}")
                    st.info(f"**Explanation:** {q.get('explanation','')}")

                    if q_idx < total - 1:
                        if st.button("Next →", use_container_width=True):
                            st.session_state.quiz_index += 1
                            st.rerun()
                    else:
                        st.balloons()
                        st.success("🎓 Quiz complete!")
            else:
                ans = st.text_area("Your answer:", height=100)
                if st.button("Submit Answer", use_container_width=True):
                    with st.spinner("Evaluating…"):
                        res = quiz_gen.evaluate_answer(q, ans)
                    session.record_question(q["question"], ans, res["is_correct"])
                    session.update_confidence(selected_topic, res["is_correct"])
                    if res["is_correct"]:
                        st.success("✅ Great answer!")
                    else:
                        st.warning("Good effort!")
                    st.info(f"**Feedback:** {res.get('feedback','')}")

    # ───── TAB 3 · Study ─────
    with tab3:
        st.markdown("#### Study Notes")
        st.caption(f"AI-generated summary for **{selected_topic}** based on NCERT content.")

        if st.button("Generate Study Notes", use_container_width=True):
            with st.spinner("Loading content…"):
                expl = explain_engine.explain_topic(
                    topic=selected_topic, class_level=session.class_level,
                    subject=session.subject)

            if expl.get("explanation"):
                st.markdown(f"### {selected_topic}")
                st.markdown(expl["explanation"])

                if expl.get("analogy"):
                    st.markdown(f"""
                    <div style="background:#fefce8;border-left:4px solid #f59e0b;
                                border-radius:0 8px 8px 0;padding:16px;margin:12px 0">
                        <b>💡 Real-world analogy</b><br>{expl['analogy']}
                    </div>
                    """, unsafe_allow_html=True)

                if expl.get("example"):
                    st.markdown(f"""
                    <div style="background:#f0fdf4;border-left:4px solid #10b981;
                                border-radius:0 8px 8px 0;padding:16px;margin:12px 0">
                        <b>📌 Example</b><br>{expl['example']}
                    </div>
                    """, unsafe_allow_html=True)

                if expl.get("key_points"):
                    st.markdown("**Key points to remember**")
                    for pt in expl["key_points"]:
                        st.markdown(f"- {pt}")

    # ───── TAB 4 · Progress ─────
    with tab4:
        st.markdown("#### Your Progress")
        summary = session.get_progress_summary()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Questions", summary["total_questions"])
        m2.metric("Accuracy",  f"{summary['accuracy']:.1f}%")
        m3.metric("Mastered",  len([v for v in summary["topic_confidence"].values() if v >= 0.7]))
        m4.metric("Session",   f"{summary['session_duration_minutes']:.0f} min")

        st.divider()

        if summary["topic_confidence"]:
            st.markdown("##### Topic Mastery")
            for topic, conf in summary["topic_confidence"].items():
                lc, rc = st.columns([4, 1])
                with lc:
                    st.progress(conf, text=topic)
                with rc:
                    badge = ("🟢 Strong" if conf >= 0.7
                             else "🟡 Building" if conf >= 0.4
                             else "🔴 Practice")
                    st.caption(badge)

        st.divider()
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("💾 Save Progress", use_container_width=True):
                os.makedirs("sessions", exist_ok=True)
                spath = f"sessions/{session.student_id}_{datetime.now():%Y%m%d_%H%M%S}.json"
                session.save_session(spath)
                st.success("Progress saved!")

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:32px 0 8px;color:#94a3b8;font-size:12px">
    <strong style="color:#64748b">EduCore</strong> · Intelligent Learning for CBSE Classes 6–10 ·
    <span>© 2025</span>
</div>
""", unsafe_allow_html=True)
