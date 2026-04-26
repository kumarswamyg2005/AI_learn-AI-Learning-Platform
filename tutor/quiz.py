"""Generate adaptive questions using Gemini or OpenAI"""

import json
import os
from typing import List, Dict

from config import LLM_PROVIDER, GEMINI_MODEL, GPT_MODEL, GEMINI_API_KEY
from rag.retriever import RAGRetriever

# Initialize LLM
if LLM_PROVIDER == "gemini":
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
else:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")


class QuizGenerator:
    """Generate adaptive questions for a topic"""

    def __init__(self):
        self.retriever = RAGRetriever()
        self.provider = LLM_PROVIDER

    def _call_llm(self, prompt: str) -> str:
        """Call LLM using configured provider"""
        try:
            if self.provider == "gemini":
                model = genai.GenerativeModel(GEMINI_MODEL)
                response = model.generate_content(prompt)
                return response.text
            else:
                response = openai.ChatCompletion.create(
                    model=GPT_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=500
                )
                return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM call failed: {e}")

    def generate_question(
        self,
        topic: str,
        difficulty: str,
        class_level: int,
        subject: str,
        question_type: str = "mcq"
    ) -> Dict:
        """
        Generate a single question using LLM with RAG context.

        Args:
            topic: Topic to generate question about
            difficulty: "easy", "medium", or "hard"
            class_level: Student's class (6-10)
            subject: Subject (Mathematics, Science, etc.)
            question_type: "mcq" or "short_answer"

        Returns:
            Dict with question, options, answer, explanation
        """
        # Get context from RAG
        context_chunks = self.retriever.retrieve_context(
            query=topic,
            subject=subject,
            class_level=class_level,
            top_k=3
        )

        context_text = "\n".join([c["text"] for c in context_chunks])

        # Difficulty descriptions
        difficulty_desc = {
            "easy": "basic concepts, straightforward facts, single-step thinking",
            "medium": "application of concepts, multi-step thinking, connecting ideas",
            "hard": "analysis and synthesis, real-world application, critical thinking"
        }

        prompt = f"""Generate a {difficulty} {question_type} question for a Class {class_level} student about "{topic}" in {subject}.

CONTEXT FROM TEXTBOOK:
{context_text[:1000]}

DIFFICULTY LEVEL: {difficulty} - questions should test {difficulty_desc.get(difficulty, "understanding")}

If generating an MCQ:
- Create 4 options (A, B, C, D)
- Only one correct answer
- Include a simple explanation

If generating a short-answer question:
- Question should be answerable in 1-2 sentences
- Include the expected answer and explanation

RESPOND IN JSON FORMAT:
{{
    "type": "{question_type}",
    "question": "The actual question text",
    "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}} or null,
    "correct_answer": "A" or "The expected answer",
    "explanation": "Why this is correct and what the student should learn",
    "difficulty": "{difficulty}"
}}
"""

        try:
            response_text = self._call_llm(prompt)
            result = json.loads(response_text)
            return result

        except json.JSONDecodeError:
            return {
                "type": question_type,
                "question": "What is the importance of this topic?",
                "options": {"A": "Important", "B": "Not important", "C": "Neutral", "D": "Complex"},
                "correct_answer": "A",
                "explanation": "Understanding all topics is important for learning.",
                "difficulty": difficulty,
                "error": "Failed to generate unique question"
            }

    def generate_quiz(
        self,
        topic: str,
        num_questions: int,
        class_level: int,
        subject: str
    ) -> List[Dict]:
        """
        Generate a complete quiz with difficulty progression.

        Args:
            topic: Topic to quiz on
            num_questions: Number of questions (typically 5)
            class_level: Student's class
            subject: Subject

        Returns:
            List of questions with increasing difficulty
        """
        difficulties = []

        # Difficulty progression: start easy, increase difficulty
        if num_questions >= 5:
            difficulties = ["easy", "easy", "medium", "hard", "hard"]
        elif num_questions == 4:
            difficulties = ["easy", "medium", "medium", "hard"]
        elif num_questions == 3:
            difficulties = ["easy", "medium", "hard"]
        elif num_questions == 2:
            difficulties = ["easy", "hard"]
        else:
            difficulties = ["medium"]

        questions = []

        for i, difficulty in enumerate(difficulties[:num_questions]):
            # Alternate between MCQ and short-answer
            question_type = "mcq" if i % 2 == 0 else "short_answer"

            question = self.generate_question(
                topic=topic,
                difficulty=difficulty,
                class_level=class_level,
                subject=subject,
                question_type=question_type
            )
            questions.append(question)

        return questions

    def evaluate_answer(self, question: Dict, student_answer: str) -> Dict:
        """
        Evaluate student's answer using LLM.

        Args:
            question: Question dict
            student_answer: Student's answer

        Returns:
            Dict with is_correct, score, feedback
        """
        prompt = f"""Evaluate this student answer to a {question['type']} question.

QUESTION: {question['question']}
EXPECTED ANSWER: {question['correct_answer']}
STUDENT ANSWER: {student_answer}
EXPLANATION: {question['explanation']}

If MCQ: Is the selected option correct?
If short-answer: Does the answer show understanding of the concept?

RESPOND IN JSON ONLY (no markdown):
{{
    "is_correct": true or false,
    "score": 0-100,
    "feedback": "Constructive feedback for the student (1-2 sentences, appropriate for Class {question.get('difficulty', 'unknown')} level)"
}}
"""

        try:
            response_text = self._call_llm(prompt)
            result = json.loads(response_text)
            return result

        except Exception as e:
            return {
                "is_correct": False,
                "score": 0,
                "feedback": "Could not evaluate answer. Please try again.",
                "error": str(e)
            }
