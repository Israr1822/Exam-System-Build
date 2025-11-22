import reflex as rx
from app.models import Attempt
from datetime import datetime


class GradingState(rx.State):
    """Manages viewing of student attempts."""

    attempts: list[Attempt] = []

    @rx.event
    def on_mount(self):
        if not self.attempts:
            self.attempts = [
                Attempt(
                    student_id=1,
                    exam_id=1,
                    score=85.5,
                    time_taken=850,
                    attempt_number=1,
                    submitted_at=datetime.now(),
                    answers={"1": "Paris", "3": "Mars"},
                ),
                Attempt(
                    student_id=2,
                    exam_id=1,
                    score=92.0,
                    time_taken=600,
                    attempt_number=1,
                    submitted_at=datetime.now(),
                    answers={"1": "Paris", "3": "Mars"},
                ),
            ]