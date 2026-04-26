"""RAG-powered explanation engine"""

import openai
from typing import Dict

from config import GPT_MODEL, MAX_RESPONSE_LENGTH
from rag.retriever import RAGRetriever

openai.api_key = openai.api_key


class ExplanationEngine:
    """Generate simple explanations with real-world analogies"""

    def __init__(self):
        self.retriever = RAGRetriever()

    def explain_topic(
        self,
        topic: str,
        class_level: int,
        subject: str,
        student_language: str = "en"
    ) -> Dict:
        """
        Explain a topic using RAG context and GPT-4.

        Args:
            topic: Topic to explain
            class_level: Student's class (6-10)
            subject: Subject (Mathematics, Science, etc.)
            student_language: Language code (en, hi, te, etc.)

        Returns:
            Dict with explanation, analogy, example, key_points
        """
        # Retrieve context from RAG
        context_chunks = self.retriever.retrieve_context(
            query=topic,
            subject=subject,
            class_level=class_level,
            top_k=5
        )

        context_text = "\n".join([c["text"] for c in context_chunks])

        if not context_text:
            return {
                "explanation": "Content not available. Please check if NCERT PDFs are loaded.",
                "analogy": None,
                "example": None,
                "key_points": []
            }

        # Generate explanation
        prompt = f"""Explain "{topic}" for a Class {class_level} student in {subject} class.

TEXTBOOK CONTENT:
{context_text[:1500]}

INSTRUCTIONS:
1. Use very simple, everyday language (as if explaining to a 12-year-old)
2. Keep explanation to ~150 words maximum
3. Include ONE real-world analogy (e.g., "Think of photosynthesis like a plant's kitchen...")
4. Provide ONE simple real-world example
5. List 3-4 key points to remember

RESPOND IN JSON FORMAT:
{{
    "explanation": "Simple explanation in 1-2 paragraphs",
    "analogy": "Real-world analogy here",
    "example": "Simple real-world example",
    "key_points": ["Point 1", "Point 2", "Point 3"]
}}
"""

        try:
            response = openai.ChatCompletion.create(
                model=GPT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=400
            )

            import json
            result = json.loads(response.choices[0].message.content)
            result["language"] = student_language
            result["topic"] = topic
            return result

        except Exception as e:
            return {
                "explanation": f"Unable to explain this topic right now. Error: {str(e)}",
                "analogy": None,
                "example": None,
                "key_points": [],
                "error": str(e)
            }

    def generate_analogy(self, topic: str, explanation: str) -> str:
        """
        Generate a real-world analogy for a topic.

        Args:
            topic: Topic name
            explanation: Current explanation of the topic

        Returns:
            A relatable analogy string
        """
        prompt = f"""Create ONE simple, relatable real-world analogy for a 12-year-old student to understand "{topic}".

TOPIC: {topic}
CURRENT EXPLANATION: {explanation}

The analogy should:
- Use something from a student's daily life (sports, cooking, playground, phone, etc.)
- Be accurate (not misleading)
- Help understand the concept deeply
- Be exactly 1-2 sentences

Example: "Photosynthesis is like cooking - plants use sunlight as heat, water as ingredients, and CO2 as more ingredients to create their own food (glucose)."

RESPOND WITH ONLY THE ANALOGY, NO JSON:
"""

        try:
            response = openai.ChatCompletion.create(
                model=GPT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=100
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Could not generate analogy: {str(e)}"

    def answer_question(
        self,
        question: str,
        subject: str,
        class_level: int
    ) -> Dict:
        """
        Answer a student's question using RAG and GPT-4.

        Args:
            question: Student's question
            subject: Subject
            class_level: Student's class

        Returns:
            Dict with answer, explanation, sources
        """
        # Retrieve relevant context
        context_chunks = self.retriever.retrieve_context(
            query=question,
            subject=subject,
            class_level=class_level,
            top_k=5
        )

        context_text = "\n".join([c["text"] for c in context_chunks])
        sources = [c["source"] for c in context_chunks[:2]]

        if not context_text:
            return {
                "answer": "I don't have information about this topic yet.",
                "explanation": "Please make sure NCERT PDFs are loaded.",
                "sources": []
            }

        prompt = f"""Answer this Class {class_level} student's question about {subject}.

STUDENT'S QUESTION: {question}

RELEVANT TEXTBOOK CONTENT:
{context_text[:1500]}

INSTRUCTIONS:
1. Give a clear, simple answer (150 words max) appropriate for Class {class_level}
2. Use everyday language
3. If helpful, include an analogy
4. Encourage further learning

RESPOND IN JSON:
{{
    "answer": "Direct answer to the question",
    "explanation": "Brief explanation or additional context",
    "analogy": "Optional analogy if helpful"
}}
"""

        try:
            response = openai.ChatCompletion.create(
                model=GPT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=300
            )

            import json
            result = json.loads(response.choices[0].message.content)
            result["sources"] = sources
            result["question"] = question
            return result

        except Exception as e:
            return {
                "answer": "Sorry, I couldn't process that question.",
                "explanation": str(e),
                "sources": [],
                "error": str(e)
            }
