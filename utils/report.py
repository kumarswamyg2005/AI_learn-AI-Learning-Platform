"""Generate progress reports for parents/teachers"""

from datetime import datetime, timedelta
from typing import Optional, Dict
import os

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class ReportGenerator:
    """Generate progress reports in PDF format"""

    def __init__(self):
        self.styles = getSampleStyleSheet() if REPORTLAB_AVAILABLE else None

    def generate_weekly_report(
        self,
        student_session,
        output_path: str = "reports/weekly_report.pdf",
        teacher_notes: Optional[str] = None
    ) -> bool:
        """
        Generate a weekly progress report in PDF.

        Args:
            student_session: StudentSession object
            output_path: Where to save the PDF
            teacher_notes: Optional notes from teacher

        Returns:
            True if successful
        """
        if not REPORTLAB_AVAILABLE:
            print("❌ reportlab not installed. Install with: pip install reportlab")
            return False

        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Create PDF
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )

            elements = []

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f77b4'),
                spaceAfter=12,
                alignment=1  # Center
            )
            elements.append(Paragraph("📊 Weekly Learning Report", title_style))
            elements.append(Spacer(1, 0.2*inch))

            # Student Info
            student_info = f"""
            <b>Student ID:</b> {student_session.student_id}<br/>
            <b>Subject:</b> {student_session.subject}<br/>
            <b>Class:</b> {student_session.class_level}<br/>
            <b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>
            """
            elements.append(Paragraph(student_info, self.styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))

            # Performance Summary
            elements.append(Paragraph("Performance Summary", self.styles['Heading2']))

            summary = student_session.get_progress_summary()
            summary_data = [
                ["Metric", "Value"],
                ["Total Questions Answered", str(summary['total_questions'])],
                ["Correct Answers", str(summary['correct_answers'])],
                ["Overall Accuracy", f"{summary['accuracy']:.1f}%"],
                ["Current Level", summary['current_level'].capitalize()],
                ["Session Duration", f"{summary['session_duration_minutes']} minutes"]
            ]

            summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))

            # Topic Breakdown
            elements.append(Paragraph("Topic Strength Breakdown", self.styles['Heading2']))

            topic_data = [["Topic", "Confidence Level", "Questions Answered"]]

            for topic, confidence in summary['topic_confidence'].items():
                topic_questions = [q for q in student_session.questions_asked if q.get("topic") == topic]
                confidence_level = "🟢 Strong" if confidence >= 0.7 else "🟡 Moderate" if confidence >= 0.4 else "🔴 Needs Work"
                topic_data.append([topic, confidence_level, str(len(topic_questions))])

            if len(topic_data) > 1:
                topic_table = Table(topic_data, colWidths=[2*inch, 2*inch, 1.5*inch])
                topic_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(topic_table)
            else:
                elements.append(Paragraph("<i>No topic data available yet</i>", self.styles['Normal']))

            elements.append(Spacer(1, 0.3*inch))

            # Recommendations
            elements.append(Paragraph("Recommendations", self.styles['Heading2']))

            recommendations = self._generate_recommendations(summary)
            for rec in recommendations:
                elements.append(Paragraph(f"• {rec}", self.styles['Normal']))

            elements.append(Spacer(1, 0.3*inch))

            # Teacher Notes
            if teacher_notes:
                elements.append(Paragraph("Teacher Notes", self.styles['Heading2']))
                elements.append(Paragraph(teacher_notes, self.styles['Normal']))

            # Footer
            elements.append(Spacer(1, 0.3*inch))
            footer = f"<i>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
            elements.append(Paragraph(footer, self.styles['Normal']))

            # Build PDF
            doc.build(elements)
            print(f"✅ Report saved to {output_path}")
            return True

        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return False

    def _generate_recommendations(self, summary: Dict) -> list:
        """Generate personalized recommendations based on performance"""
        recommendations = []

        accuracy = summary['accuracy']

        if accuracy >= 80:
            recommendations.append("Excellent progress! Continue practicing harder topics.")
        elif accuracy >= 60:
            recommendations.append("Good work! Focus on topics with lower confidence levels.")
        else:
            recommendations.append("Keep practicing! Start with easier topics to build confidence.")

        if summary['current_level'] == 'hard':
            recommendations.append("Student is ready for advanced topics and challenging problems.")
        elif summary['current_level'] == 'easy':
            recommendations.append("Student would benefit from more practice on fundamentals.")

        recommendations.append("Regular practice (15-20 min daily) shows the best results.")

        if summary['total_questions'] < 10:
            recommendations.append("Encourage more practice sessions for better learning outcomes.")

        return recommendations

    def generate_monthly_summary(
        self,
        student_sessions: list,
        output_path: str = "reports/monthly_summary.pdf"
    ) -> bool:
        """
        Generate a monthly summary of multiple sessions.

        Args:
            student_sessions: List of StudentSession objects
            output_path: Where to save the PDF

        Returns:
            True if successful
        """
        if not REPORTLAB_AVAILABLE:
            return False

        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            doc = SimpleDocTemplate(output_path, pagesize=A4)
            elements = []

            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f77b4'),
                spaceAfter=12,
                alignment=1
            )

            elements.append(Paragraph("📈 Monthly Learning Summary", title_style))
            elements.append(Spacer(1, 0.2*inch))

            # Aggregate statistics
            total_sessions = len(student_sessions)
            total_questions = sum(s.correct_answers + s.incorrect_answers for s in student_sessions)
            total_correct = sum(s.correct_answers for s in student_sessions)
            avg_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0

            summary_text = f"""
            <b>Summary Statistics (Month of {datetime.now().strftime('%B %Y')})</b><br/>
            Total Learning Sessions: {total_sessions}<br/>
            Total Questions: {total_questions}<br/>
            Overall Accuracy: {avg_accuracy:.1f}%<br/>
            """

            elements.append(Paragraph(summary_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))

            # Session details
            for session in student_sessions:
                summary = session.get_progress_summary()
                session_text = f"""
                <b>{session.subject} - Class {session.class_level}</b><br/>
                Accuracy: {summary['accuracy']:.1f}% | Level: {summary['current_level']} | Questions: {summary['total_questions']}<br/>
                """
                elements.append(Paragraph(session_text, self.styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))

            doc.build(elements)
            print(f"✅ Monthly summary saved to {output_path}")
            return True

        except Exception as e:
            print(f"❌ Error generating monthly summary: {e}")
            return False
