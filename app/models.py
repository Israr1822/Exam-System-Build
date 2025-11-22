import reflex as rx
from typing import Optional
from datetime import datetime


class Question(rx.Base):
    """Model for storing exam questions."""

    id: int = 0
    question_text: str = ""
    question_type: str = "MCQ"
    category: str = "General"
    marks: int = 1
    feedback: str = ""
    mcq_options: list[str] = ["", "", "", ""]
    correct_answer: str = ""
    short_answer_config: dict[str, str | int | float | bool] = {}


class Exam(rx.Base):
    """Model for storing exam definitions."""

    title: str
    categories: list[str] = []
    question_ids: list[int] = []
    exam_type: str
    duration: int = 0
    created_at: datetime = datetime.now()


class Student(rx.Base):
    """Model for students."""

    email: str
    password: str
    name: str
    created_at: datetime = datetime.now()


class Attempt(rx.Base):
    """Model for student exam attempts."""

    student_id: int
    exam_id: int
    answers: dict[str, str] = {}
    score: float = 0.0
    time_taken: int = 0
    attempt_number: int
    submitted_at: datetime = datetime.now()
    bookmarks: list[int] = []


class ReviewSettings(rx.Base):
    """Model for exam review configurations."""

    exam_id: int
    review_enabled: bool = False
    exam_mode: str = "assessment"


class Assignment(rx.Base):
    """Model for assigning exams to students."""

    exam_id: int
    student_id: int
    attempts_allowed: int = 1
    attempts_used: int = 0
    expiry_date: Optional[datetime] = None
    assigned_at: datetime = datetime.now()
    disabled: bool = False


class Admin(rx.Base):
    """Model for admin users."""

    email: str
    password: str