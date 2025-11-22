import reflex as rx
from typing import Optional
from app.models import Admin


class AuthState(rx.State):
    """Manages authentication state for the application."""

    email: str = ""
    password: str = ""
    is_authenticated: bool = False
    user_role: Optional[str] = None
    error_message: str = ""

    @rx.event
    def on_load_admin(self):
        """Check if user is authenticated as admin, otherwise redirect."""
        if not self.is_authenticated or self.user_role != "admin":
            return rx.redirect("/admin/login")

    @rx.event
    def on_load_student(self):
        """Check if user is authenticated as student, otherwise redirect."""
        if not self.is_authenticated or self.user_role != "student":
            return rx.redirect("/student/login")

    @rx.event
    async def admin_login(self, form_data: dict):
        """Handle admin login."""
        email = form_data.get("email", "")
        password = form_data.get("password", "")
        if email == "admin@example.com" and password == "admin":
            self.email = email
            self.is_authenticated = True
            self.user_role = "admin"
            self.error_message = ""
            return rx.redirect("/admin/dashboard")
        self.error_message = "Invalid credentials. Try admin@example.com / admin"

    @rx.event
    async def student_login(self, form_data: dict):
        """Handle student login."""
        from app.states.student_state import StudentState

        student_state = await self.get_state(StudentState)
        email = form_data.get("email", "")
        password = form_data.get("password", "")
        student = next(
            (
                s
                for s in student_state.students
                if s.email == email and s.password == password
            ),
            None,
        )
        if student:
            self.email = email
            self.is_authenticated = True
            self.user_role = "student"
            self.error_message = ""
            return rx.redirect("/student/dashboard")
        self.error_message = "Invalid email or password."

    @rx.event
    async def student_register(self, form_data: dict):
        """Handle student registration."""
        from app.states.student_state import StudentState

        student_state = await self.get_state(StudentState)
        name = form_data.get("name", "")
        email = form_data.get("email", "")
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")
        if password != confirm_password:
            self.error_message = "Passwords do not match."
            return
        if any((s.email == email for s in student_state.students)):
            self.error_message = "Email already registered."
            return
        from app.models import Student
        from datetime import datetime

        new_student = Student(
            name=name, email=email, password=password, created_at=datetime.now()
        )
        student_state.students.append(new_student)
        self.email = email
        self.is_authenticated = True
        self.user_role = "student"
        self.error_message = ""
        return rx.redirect("/student/dashboard")

    @rx.event
    def logout(self):
        """Handle logout."""
        self.is_authenticated = False
        self.user_role = None
        self.email = ""
        self.password = ""
        return rx.redirect("/")