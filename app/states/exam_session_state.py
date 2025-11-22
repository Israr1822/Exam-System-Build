import reflex as rx
import asyncio
import logging
from typing import Optional, Any
from datetime import datetime
from app.models import Exam, Question, Attempt
from app.states.auth_state import AuthState
from app.states.exam_state import ExamState
from app.states.question_state import QuestionState
from app.states.assignment_state import AssignmentState


class ExamSessionState(rx.State):
    """Manages the state of an active exam session."""

    exam_id: int = 0
    exam_title: str = ""
    exam_duration: int = 0
    is_timed: bool = False
    questions: list[Question] = []
    current_question_index: int = 0
    answers: dict[str, str] = {}
    bookmarks: list[int] = []
    time_remaining: int = 0
    timer_active: bool = False
    is_submitting: bool = False
    confirm_submit_open: bool = False

    @rx.var
    def current_question(self) -> Optional[Question]:
        if 0 <= self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    @rx.var
    def formatted_time(self) -> str:
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        return f"{minutes:02d}:{seconds:02d}"

    @rx.var
    def progress_percentage(self) -> int:
        if not self.questions:
            return 0
        answered_count = 0
        for q in self.questions:
            if str(q.id) in self.answers and self.answers[str(q.id)]:
                answered_count += 1
        return int(answered_count / len(self.questions) * 100)

    @rx.event
    async def load_exam(self):
        """Initialize the exam session."""
        args = self.router.page.params
        e_id_str = args.get("e_id", "0")
        try:
            self.exam_id = int(e_id_str)
        except ValueError as e:
            logging.exception(f"Invalid exam ID: {e}")
            return rx.redirect("/student/dashboard")
        if self.exam_id <= 0:
            return rx.redirect("/student/dashboard")
        exam_state = await self.get_state(ExamState)
        q_state = await self.get_state(QuestionState)
        if self.exam_id > len(exam_state.exams):
            return rx.redirect("/student/dashboard")
        exam = exam_state.exams[self.exam_id - 1]
        self.exam_title = exam.title
        self.exam_duration = exam.duration
        self.is_timed = exam.exam_type == "Timed"
        self.time_remaining = exam.duration * 60
        self.questions = [q for q in q_state.questions if q.id in exam.question_ids]
        self.current_question_index = 0
        self.answers = {}
        self.bookmarks = []
        self.is_submitting = False
        self.confirm_submit_open = False
        if self.is_timed:
            self.timer_active = True
            return ExamSessionState.tick

    @rx.event(background=True)
    async def tick(self):
        """Countdown timer tick."""
        while True:
            async with self:
                if not self.timer_active or self.time_remaining <= 0:
                    if self.timer_active and self.time_remaining <= 0:
                        self.timer_active = False
                        return ExamSessionState.submit_exam
                    return
                self.time_remaining -= 1
            await asyncio.sleep(1)

    @rx.event
    def set_answer(self, value: str):
        if self.current_question:
            self.answers[str(self.current_question.id)] = value

    @rx.event
    def toggle_bookmark(self):
        if self.current_question:
            q_id = self.current_question.id
            if q_id in self.bookmarks:
                self.bookmarks.remove(q_id)
            else:
                self.bookmarks.append(q_id)

    @rx.event
    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1

    @rx.event
    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1

    @rx.event
    def jump_to_question(self, index: int):
        if 0 <= index < len(self.questions):
            self.current_question_index = index

    @rx.event
    def open_submit_modal(self):
        self.confirm_submit_open = True

    @rx.event
    def close_submit_modal(self):
        self.confirm_submit_open = False

    @rx.event
    async def submit_exam(self):
        self.timer_active = False
        self.confirm_submit_open = False
        self.is_submitting = True
        total_score = 0.0
        total_marks = 0
        for q in self.questions:
            total_marks += q.marks
            user_ans = self.answers.get(q.id, "")
            if q.question_type == "MCQ":
                if user_ans == q.correct_answer:
                    total_score += q.marks
            elif q.question_type == "Short Answer":
                try:
                    correct_val = int(q.correct_answer)
                    user_val = int(user_ans)
                    tol_min = q.short_answer_config.get("tolerance_min", 0)
                    tol_max = q.short_answer_config.get("tolerance_max", 0)
                    if correct_val - tol_min <= user_val <= correct_val + tol_max:
                        total_score += q.marks
                except ValueError as e:
                    logging.exception(f"Error grading short answer: {e}")
        final_score_percent = (
            round(total_score / total_marks * 100, 1) if total_marks > 0 else 0
        )
        from app.states.student_state import StudentState
        from app.states.grading_state import GradingState

        auth_state = await self.get_state(AuthState)
        student_state = await self.get_state(StudentState)
        student_id = -1
        for idx, s in enumerate(student_state.students):
            if s.email == auth_state.email:
                student_id = idx + 1
                break
        attempt = Attempt(
            student_id=student_id,
            exam_id=self.exam_id,
            answers=self.answers,
            score=final_score_percent,
            time_taken=self.exam_duration * 60 - self.time_remaining
            if self.is_timed
            else 0,
            attempt_number=1,
            submitted_at=datetime.now(),
            bookmarks=self.bookmarks,
        )
        grading_state = await self.get_state(GradingState)
        grading_state.attempts.append(attempt)
        assignment_state = await self.get_state(AssignmentState)
        for a in assignment_state.assignments:
            if a.exam_id == self.exam_id and a.student_id == student_id:
                a.attempts_used += 1
                break
        return rx.redirect(f"/student/exam/{self.exam_id}/result")