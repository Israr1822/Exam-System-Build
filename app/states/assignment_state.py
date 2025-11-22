import reflex as rx
from app.models import Assignment
from datetime import datetime, timedelta
from typing import Optional


class AssignmentState(rx.State):
    """Manages exam assignments to students."""

    assignments: list[Assignment] = []
    is_modal_open: bool = False
    selected_exam_title: str = ""
    selected_student_email: str = ""
    form_attempts: int = 1
    form_expiry_days: int = 7

    @rx.event
    def on_mount(self):
        if not self.assignments:
            self.assignments = [
                Assignment(
                    exam_id=1,
                    student_id=1,
                    attempts_allowed=2,
                    attempts_used=0,
                    expiry_date=datetime.now() + timedelta(days=5),
                    disabled=False,
                )
            ]

    @rx.event
    def open_assign_modal(self, exam_title: str = ""):
        self.selected_exam_title = exam_title
        self.selected_student_email = ""
        self.form_attempts = 1
        self.form_expiry_days = 7
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False

    @rx.event
    def create_assignment(self):
        if not self.selected_exam_title or not self.selected_student_email:
            return rx.window_alert("Please select both an exam and a student")
        new_assignment = Assignment(
            exam_id=0,
            student_id=0,
            attempts_allowed=self.form_attempts,
            attempts_used=0,
            expiry_date=datetime.now() + timedelta(days=self.form_expiry_days),
            disabled=False,
        )
        self.assignments.append(new_assignment)
        self.is_modal_open = False
        return rx.toast.success(
            f"Exam '{self.selected_exam_title}' assigned to {self.selected_student_email}"
        )

    @rx.event
    def toggle_assignment_status(self, assignment: Assignment):
        assignment.disabled = not assignment.disabled
        pass