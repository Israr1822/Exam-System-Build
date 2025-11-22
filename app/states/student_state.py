import reflex as rx
from app.models import Student
from datetime import datetime
import random
import string


class StudentState(rx.State):
    """Manages student state."""

    students: list[Student] = []
    search_query: str = ""
    is_modal_open: bool = False
    form_name: str = ""
    form_email: str = ""
    form_password: str = ""

    @rx.event
    def on_mount(self):
        """Initialize with sample data if empty."""
        if not self.students:
            self.students = [
                Student(
                    name="Alice Smith",
                    email="alice@example.com",
                    password="password123",
                    created_at=datetime.now(),
                ),
                Student(
                    name="Bob Jones",
                    email="bob@example.com",
                    password="password123",
                    created_at=datetime.now(),
                ),
                Student(
                    name="Charlie Brown",
                    email="charlie@example.com",
                    password="password123",
                    created_at=datetime.now(),
                ),
            ]

    @rx.var
    def filtered_students(self) -> list[Student]:
        """Filter students by search query."""
        if not self.search_query:
            return self.students
        query = self.search_query.lower()
        return [
            s
            for s in self.students
            if query in s.name.lower() or query in s.email.lower()
        ]

    @rx.event
    def open_add_modal(self):
        self.form_name = ""
        self.form_email = ""
        self.form_password = ""
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False

    @rx.event
    def save_student(self):
        if not self.form_name or not self.form_email or (not self.form_password):
            return rx.window_alert("All fields are required")
        if any((s.email == self.form_email for s in self.students)):
            return rx.window_alert("Email already exists")
        new_student = Student(
            name=self.form_name,
            email=self.form_email,
            password=self.form_password,
            created_at=datetime.now(),
        )
        self.students.insert(0, new_student)
        self.is_modal_open = False
        return rx.toast.info("Student added successfully")

    @rx.event
    def delete_student(self, email: str):
        self.students = [s for s in self.students if s.email != email]