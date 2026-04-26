"""Student session management"""

class StudentSession:
    """Track student's progress, confidence, and learning state"""
    
    def __init__(self, student_id, subject, class_level):
        self.student_id = student_id
        self.subject = subject
        self.class_level = class_level
        self.current_topic = None
        self.questions_asked = []
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.topic_confidence = {}  # {topic: confidence (0-100)}
    
    def update_confidence(self, topic, score, correct):
        """Update confidence level for a topic based on answer"""
        # TODO: Adjust confidence using exponential moving average
        pass
    
    def get_current_level(self):
        """Return current difficulty level (Easy/Medium/Hard)"""
        # TODO: Based on confidence scores
        pass
