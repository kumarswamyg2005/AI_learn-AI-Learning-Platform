"""Student session management"""

from datetime import datetime
from typing import Dict, List
import json
import os


class StudentSession:
    """Track student's progress, confidence, and learning state"""

    def __init__(self, student_id: str, subject: str, class_level: int):
        self.student_id = student_id
        self.subject = subject
        self.class_level = class_level
        self.current_topic = None
        self.questions_asked: List[Dict] = []
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.topic_confidence: Dict[str, float] = {}  # {topic: confidence (0-1)}
        self.session_start = datetime.now()
        self.last_activity = datetime.now()

    def set_topic(self, topic: str) -> None:
        """Set current learning topic"""
        self.current_topic = topic
        if topic not in self.topic_confidence:
            self.topic_confidence[topic] = 0.5
        self.last_activity = datetime.now()

    def record_question(self, question: str, answer: str, correct: bool, difficulty: str = "medium") -> None:
        """Record a question asked during the session"""
        self.questions_asked.append({
            "question": question,
            "answer": answer,
            "correct": correct,
            "difficulty": difficulty,
            "timestamp": datetime.now().isoformat(),
            "topic": self.current_topic
        })

        if correct:
            self.correct_answers += 1
        else:
            self.incorrect_answers += 1

        self.last_activity = datetime.now()

    def update_confidence(self, topic: str, is_correct: bool) -> None:
        """
        Update confidence level using exponential moving average.
        Confidence increases by +0.1 on correct, decreases by -0.15 on incorrect.
        """
        if topic not in self.topic_confidence:
            self.topic_confidence[topic] = 0.5

        current = self.topic_confidence[topic]
        alpha = 0.3  # EMA smoothing factor

        if is_correct:
            new_confidence = current + 0.1
        else:
            new_confidence = current - 0.15

        # Clamp between 0 and 1
        self.topic_confidence[topic] = max(0.0, min(1.0, new_confidence))
        self.last_activity = datetime.now()

    def get_current_level(self) -> str:
        """Return current difficulty level based on confidence"""
        if not self.current_topic:
            return "medium"

        confidence = self.topic_confidence.get(self.current_topic, 0.5)

        if confidence >= 0.7:
            return "hard"
        elif confidence <= 0.4:
            return "easy"
        else:
            return "medium"

    def get_accuracy(self) -> float:
        """Get overall accuracy percentage"""
        total = self.correct_answers + self.incorrect_answers
        if total == 0:
            return 0.0
        return (self.correct_answers / total) * 100

    def get_topic_accuracy(self, topic: str) -> float:
        """Get accuracy for a specific topic"""
        topic_questions = [q for q in self.questions_asked if q["topic"] == topic]
        if not topic_questions:
            return 0.0
        correct = sum(1 for q in topic_questions if q["correct"])
        return (correct / len(topic_questions)) * 100

    def get_progress_summary(self) -> Dict:
        """Get summary of student's progress"""
        return {
            "student_id": self.student_id,
            "subject": self.subject,
            "class": self.class_level,
            "total_questions": len(self.questions_asked),
            "correct_answers": self.correct_answers,
            "incorrect_answers": self.incorrect_answers,
            "accuracy": self.get_accuracy(),
            "current_topic": self.current_topic,
            "current_level": self.get_current_level(),
            "topic_confidence": {t: round(c, 2) for t, c in self.topic_confidence.items()},
            "session_duration_minutes": round((datetime.now() - self.session_start).total_seconds() / 60, 1)
        }

    def save_session(self, filepath: str) -> None:
        """Save session to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data = {
            "student_id": self.student_id,
            "subject": self.subject,
            "class": self.class_level,
            "session_start": self.session_start.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "current_topic": self.current_topic,
            "correct_answers": self.correct_answers,
            "incorrect_answers": self.incorrect_answers,
            "topic_confidence": self.topic_confidence,
            "questions_asked": self.questions_asked
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_session(cls, filepath: str) -> "StudentSession":
        """Load session from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        session = cls(data["student_id"], data["subject"], data["class"])
        session.session_start = datetime.fromisoformat(data["session_start"])
        session.last_activity = datetime.fromisoformat(data["last_activity"])
        session.current_topic = data["current_topic"]
        session.correct_answers = data["correct_answers"]
        session.incorrect_answers = data["incorrect_answers"]
        session.topic_confidence = data["topic_confidence"]
        session.questions_asked = data["questions_asked"]

        return session
