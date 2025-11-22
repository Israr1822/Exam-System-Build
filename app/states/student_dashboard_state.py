import reflex as rx
from typing import TypedDict
from datetime import datetime
from app.models import Assignment, Exam
from app.states.auth_state import AuthState
from app.states.assignment_state import AssignmentState
from app.states.exam_state import ExamState


class StudentAssignmentDisplay(TypedDict):
    exam_id: int
    exam_title: str
    exam_type: str
    duration: int
    attempts_left: int
    expiry_date: str
    status: str


class StudentDashboardState(rx.State):
    """Manages the student dashboard state."""

    assignments_display: list[StudentAssignmentDisplay] = []

    @rx.event
    async def on_load(self):
        """Load student assignments."""
        auth_state = await self.get_state(AuthState)
        assignment_state = await self.get_state(AssignmentState)
        exam_state = await self.get_state(ExamState)
        current_student_email = auth_state.email
        from app.states.student_state import StudentState

        student_state = await self.get_state(StudentState)
        student_id = -1
        for idx, s in enumerate(student_state.students):
            if s.email == current_student_email:
                student_id = idx + 1
                break
        if student_id == -1:
            self.assignments_display = []
            return
        my_assignments = [
            a
            for a in assignment_state.assignments
            if a.student_id == student_id and (not a.disabled)
        ]
        display_list = []
        for assign in my_assignments:
            exam = next((e for e in exam_state.exams if e.question_ids and True), None)
            if assign.exam_id > 0 and assign.exam_id <= len(exam_state.exams):
                exam = exam_state.exams[assign.exam_id - 1]
                attempts_left = assign.attempts_allowed - assign.attempts_used
                is_expired = assign.expiry_date and assign.expiry_date < datetime.now()
                status = "Available"
                if is_expired:
                    status = "Expired"
                elif attempts_left <= 0:
                    status = "Completed"
                display_list.append(
                    {
                        "exam_id": assign.exam_id,
                        "exam_title": exam.title,
                        "exam_type": exam.exam_type,
                        "duration": exam.duration,
                        "attempts_left": attempts_left,
                        "expiry_date": assign.expiry_date.strftime("%Y-%m-%d")
                        if assign.expiry_date
                        else "Never",
                        "status": status,
                    }
                )
        self.assignments_display = display_list

    @rx.event
    def start_exam(self, exam_id: int):
        return rx.redirect(f"/student/exam/{exam_id}")