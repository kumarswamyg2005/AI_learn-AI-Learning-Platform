"""Demo script showing AI Tutor in action"""

from tutor.session import StudentSession
from tutor.quiz import QuizGenerator
from tutor.explain import ExplanationEngine
from rag.retriever import RAGRetriever

def demo():
    """Run a demo of the AI tutor"""
    print("\n🎓 AI TUTOR DEMO")
    print("=" * 50)

    # Create student session
    student = StudentSession(
        student_id="demo_student",
        subject="Mathematics",
        class_level=7
    )

    print(f"\n✅ Created session for: {student.student_id}")
    print(f"   Subject: {student.subject}")
    print(f"   Class: {student.class_level}")

    # Set topic
    topic = "Fractions"
    student.set_topic(topic)
    print(f"\n📖 Current Topic: {topic}")

    # Initialize components
    retriever = RAGRetriever()
    explain_engine = ExplanationEngine()
    quiz_gen = QuizGenerator()

    # 1. Retrieve relevant content
    print(f"\n🔍 Retrieving content about {topic}...")
    chunks = retriever.retrieve_context(
        query=topic,
        subject="Mathematics",
        class_level=7,
        top_k=3
    )

    if chunks:
        print(f"   Found {len(chunks)} relevant chunks from NCERT")
        for i, chunk in enumerate(chunks, 1):
            print(f"   [{i}] Chapter: {chunk['chapter']} (similarity: {chunk['similarity']:.2f})")
    else:
        print("   ℹ️  No chunks found - ensure NCERT PDFs are loaded with: python init_rag.py")

    # 2. Get explanation
    print(f"\n📚 Getting explanation for {topic}...")
    explanation = explain_engine.explain_topic(
        topic=topic,
        class_level=7,
        subject="Mathematics"
    )

    if explanation.get("explanation"):
        print(f"\n💡 Explanation:")
        print(f"   {explanation['explanation'][:200]}...")
        if explanation.get("analogy"):
            print(f"\n🎯 Analogy: {explanation['analogy']}")
    else:
        print("   ⚠️  Could not generate explanation - check API keys")

    # 3. Generate quiz questions
    print(f"\n📝 Generating quiz questions...")
    try:
        questions = quiz_gen.generate_quiz(
            topic=topic,
            num_questions=3,
            class_level=7,
            subject="Mathematics"
        )

        print(f"   Generated {len(questions)} questions")

        for i, q in enumerate(questions, 1):
            print(f"\n   Question {i} ({q.get('difficulty', 'unknown')} - {q.get('type')})")
            print(f"   {q.get('question', 'N/A')[:100]}...")

    except Exception as e:
        print(f"   ⚠️  Could not generate questions: {e}")
        print("   ℹ️  Ensure OPENAI_API_KEY is set")

    # 4. Record learning activity
    print(f"\n📊 Recording learning activity...")
    student.record_question(
        question=f"What is {topic}?",
        answer="A part of a whole",
        correct=True,
        difficulty="easy"
    )

    student.update_confidence(topic, True)

    summary = student.get_progress_summary()
    print(f"   Questions answered: {summary['total_questions']}")
    print(f"   Accuracy: {summary['accuracy']:.1f}%")
    print(f"   Confidence in {topic}: {summary['topic_confidence'].get(topic, 0):.2f}")

    print("\n" + "=" * 50)
    print("✅ Demo complete!")
    print("\n📌 Next steps:")
    print("   1. Set OPENAI_API_KEY to enable AI features")
    print("   2. Run 'python init_rag.py' to load NCERT PDFs")
    print("   3. Run 'streamlit run app.py' to start the web interface")
    print("\n")

if __name__ == "__main__":
    demo()
