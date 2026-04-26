"""Main Streamlit application for AI Tutor"""

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

st.set_page_config(
    page_title="🎓 AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
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

st.title("🎓 AI Tutor for Underprivileged Students")
st.markdown("Learn NCERT curriculum with AI-powered personalized tutoring")

# Sidebar
with st.sidebar:
    st.header("📚 Setup")

    # Student info
    student_id = st.text_input("Your Name/ID", value="Student", key="student_id")

    selected_class = st.selectbox(
        "Select Class",
        CLASSES,
        format_func=lambda x: f"Class {x}"
    )

    selected_subject = st.selectbox(
        "Select Subject",
        list(SUBJECTS.keys())
    )

    # Create or load session
    if st.button("🎯 Start Learning", use_container_width=True):
        st.session_state.student_session = StudentSession(
            student_id=student_id,
            subject=selected_subject,
            class_level=selected_class
        )
        st.success(f"👋 Welcome {student_id}!")

    # Progress tracker
    st.markdown("---")
    st.header("📊 Progress Tracker")

    if st.session_state.student_session:
        summary = st.session_state.student_session.get_progress_summary()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Accuracy", f"{summary['accuracy']:.1f}%")
        with col2:
            st.metric("Questions", summary['total_questions'])

        # Topic confidence radar chart
        if summary['topic_confidence']:
            topics = list(summary['topic_confidence'].keys())
            confidences = [summary['topic_confidence'][t] * 100 for t in topics]

            fig = go.Figure(data=go.Scatterpolar(
                r=confidences,
                theta=topics,
                fill='toself',
                name='Confidence'
            ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                height=400,
                margin=dict(l=50, r=50, t=50, b=50)
            )

            st.plotly_chart(fig, use_container_width=True)

    # Teacher/Parent View
    st.markdown("---")
    st.header("👨‍🏫 Reports")

    if st.session_state.student_session:
        if st.button("📄 Generate Weekly Report", use_container_width=True):
            report_path = f"reports/{st.session_state.student_session.student_id}_report.pdf"
            if report_gen.generate_weekly_report(
                st.session_state.student_session,
                report_path
            ):
                with open(report_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download Report",
                        data=f.read(),
                        file_name=os.path.basename(report_path),
                        mime="application/pdf"
                    )

    # Language selection
    st.markdown("---")
    st.header("🌐 Language")
    language = st.selectbox(
        "Response Language",
        ["English", "Hindi", "Telugu"],
        key="language"
    )
    language_map = {"English": "en", "Hindi": "hi", "Telugu": "te"}
    selected_language = language_map[language]

# Main content
if not st.session_state.student_session:
    st.info("👈 Please select your class and subject, then click 'Start Learning' to begin!")

else:
    session = st.session_state.student_session

    col1, col2 = st.columns([3, 1])
    with col1:
        st.header(f"📚 {session.subject} - Class {session.class_level}")
    with col2:
        st.metric("Current Level", session.get_current_level().upper())

    # Topic selection
    topics = SUBJECTS.get(session.subject, [])
    selected_topic = st.selectbox("📖 Select Topic", topics, key="topic")

    if selected_topic:
        session.set_topic(selected_topic)

    # Main interface - Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Ask Questions", "📝 Quiz", "📖 Learn", "📊 My Progress"])

    # Tab 1: Ask Questions
    with tab1:
        st.header("💬 Ask Your Questions")

        # Text input
        user_question = st.text_input(
            "Ask a question about the topic:",
            placeholder=f"e.g., What is {selected_topic}?",
            key="question_input"
        )

        # Voice input (if available)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("Or record your question (coming soon with audio support)")
        with col2:
            st.write("")  # Spacer

        if user_question:
            st.session_state.messages.append({"role": "user", "content": user_question})

            with st.spinner("🤔 Thinking..."):
                # Get answer using explanation engine
                response = explain_engine.answer_question(
                    question=user_question,
                    subject=session.subject,
                    class_level=session.class_level
                )

                # Translate if needed
                if selected_language != "en":
                    response = format_response_multilingual(response, selected_language)

                # Store in session
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.get("answer", "Could not answer")
                })

            # Display chat
            st.subheader("Chat History")
            for msg in st.session_state.messages[-4:]:  # Last 4 messages
                with st.chat_message(msg["role"]):
                    if isinstance(msg.get("content"), dict):
                        st.markdown(msg["content"].get("answer", str(msg["content"])))
                    else:
                        st.markdown(msg["content"])

            # Show explanation and analogy
            if isinstance(response, dict) and response.get("answer"):
                st.info(f"💡 **Explanation**: {response.get('explanation', 'N/A')}")
                if response.get("analogy"):
                    st.success(f"🎯 **Analogy**: {response.get('analogy')}")

    # Tab 2: Quiz
    with tab2:
        st.header("📝 Test Yourself")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Generate 5-Question Quiz", use_container_width=True):
                st.session_state.quiz_active = True
                st.session_state.quiz_index = 0

                with st.spinner("Generating questions..."):
                    st.session_state.quiz_questions = quiz_gen.generate_quiz(
                        topic=selected_topic,
                        num_questions=5,
                        class_level=session.class_level,
                        subject=session.subject
                    )

                st.success("✅ Quiz generated! Start answering below.")

        if st.session_state.quiz_active and st.session_state.quiz_questions:
            q_idx = st.session_state.quiz_index
            question = st.session_state.quiz_questions[q_idx]

            st.write(f"**Question {q_idx + 1}/5**")
            st.write(f"**Level: {question.get('difficulty', 'medium').upper()}**")
            st.write(f"\n{question['question']}")

            # Display options or input based on type
            if question['type'] == 'mcq':
                options = question.get('options', {})
                if options:
                    selected_answer = st.radio(
                        "Choose your answer:",
                        list(options.keys()),
                        format_func=lambda x: f"{x}: {options[x]}"
                    )

                    if st.button("Submit Answer", use_container_width=True):
                        with st.spinner("Evaluating..."):
                            result = quiz_gen.evaluate_answer(question, selected_answer)

                        st.session_state.messages.append({
                            "role": "user",
                            "content": f"Q{q_idx + 1}: {selected_answer}"
                        })

                        session.record_question(
                            question=question['question'],
                            answer=selected_answer,
                            correct=result['is_correct'],
                            difficulty=question.get('difficulty', 'medium')
                        )

                        session.update_confidence(selected_topic, result['is_correct'])

                        # Show result
                        if result['is_correct']:
                            st.success(f"✅ Correct! {result.get('feedback', '')}")
                        else:
                            st.error(f"❌ Incorrect. {result.get('feedback', '')}")

                        st.info(f"**Explanation**: {question.get('explanation', '')}")

                        # Next button
                        if q_idx < 4:
                            if st.button("Next Question →", use_container_width=True):
                                st.session_state.quiz_index += 1
                                st.rerun()
                        else:
                            st.success("🎉 Quiz Complete!")
                            summary = session.get_progress_summary()
                            st.metric("Quiz Accuracy", f"{summary['accuracy']:.1f}%")

                            if st.button("Take Another Quiz", use_container_width=True):
                                st.session_state.quiz_active = False
                                st.rerun()

            else:  # Short answer
                student_answer = st.text_area("Your answer:", height=100)

                if st.button("Submit Answer", use_container_width=True):
                    with st.spinner("Evaluating..."):
                        result = quiz_gen.evaluate_answer(question, student_answer)

                    session.record_question(
                        question=question['question'],
                        answer=student_answer,
                        correct=result['is_correct'],
                        difficulty=question.get('difficulty', 'medium')
                    )

                    session.update_confidence(selected_topic, result['is_correct'])

                    st.write("### Evaluation")
                    if result['is_correct']:
                        st.success(f"✅ Good Answer!")
                    else:
                        st.warning("Partially correct or incorrect")

                    st.info(f"**Feedback**: {result.get('feedback', 'N/A')}")
                    st.info(f"**Explanation**: {question.get('explanation', '')}")

                    if q_idx < 4:
                        if st.button("Next Question →", use_container_width=True):
                            st.session_state.quiz_index += 1
                            st.rerun()

    # Tab 3: Learn
    with tab3:
        st.header("📖 Learn This Topic")

        if st.button("Get Explanation", use_container_width=True):
            with st.spinner("Generating explanation..."):
                explanation = explain_engine.explain_topic(
                    topic=selected_topic,
                    class_level=session.class_level,
                    subject=session.subject,
                    student_language=selected_language
                )

            if explanation.get("explanation"):
                st.markdown(f"### {selected_topic}")
                st.write(explanation["explanation"])

                if explanation.get("analogy"):
                    st.success(f"**Think of it like**: {explanation['analogy']}")

                if explanation.get("example"):
                    st.info(f"**Real-world example**: {explanation['example']}")

                if explanation.get("key_points"):
                    st.write("**Key Points to Remember**:")
                    for point in explanation["key_points"]:
                        st.write(f"• {point}")

    # Tab 4: Progress
    with tab4:
        st.header("📊 Your Learning Progress")

        summary = session.get_progress_summary()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Questions", summary['total_questions'])
        with col2:
            st.metric("Correct Answers", summary['correct_answers'])
        with col3:
            st.metric("Accuracy", f"{summary['accuracy']:.1f}%")

        st.subheader("Topic Strengths")
        if summary['topic_confidence']:
            for topic, confidence in summary['topic_confidence'].items():
                confidence_pct = confidence * 100
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.progress(confidence, text=topic)
                with col2:
                    if confidence >= 0.7:
                        st.write("🟢 Strong")
                    elif confidence >= 0.4:
                        st.write("🟡 Medium")
                    else:
                        st.write("🔴 Needs Work")

        st.subheader("Session Statistics")
        st.write(f"Session Duration: {summary['session_duration_minutes']} minutes")
        st.write(f"Current Level: **{summary['current_level'].upper()}**")

        if st.button("Save Session", use_container_width=True):
            session_path = f"sessions/{session.student_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs("sessions", exist_ok=True)
            session.save_session(session_path)
            st.success(f"✅ Session saved to {session_path}")

# Footer
st.markdown("---")
st.markdown("""
**🎓 AI Tutor for Underprivileged Students**

Built with ❤️ for educational equity
- NCERT Curriculum (Class 6-10)
- Adaptive Learning with AI
- Multilingual Support
- Voice & Text Interaction

[NCERT Official](https://ncert.nic.in) | [GitHub](https://github.com) | Report Issues
""")
