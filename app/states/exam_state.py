import reflex as rx
import logging
from app.models import Exam, Question
from datetime import datetime
from app.states.question_state import QuestionState


class ExamState(rx.State):
    """Manages exam state."""

    exams: list[Exam] = []
    is_modal_open: bool = False
    is_editing: bool = False
    current_exam_index: int = -1
    form_title: str = ""
    form_duration: int = 30
    form_type: str = "Timed"
    form_category_filter: str = "All"
    form_selected_question_ids: list[int] = []
    available_questions: list[Question] = []

    @rx.event
    async def on_mount(self):
        """Load initial data."""
        if not self.exams:
            self.exams = [
                Exam(
                    title="General Knowledge Basics",
                    categories=["General", "History"],
                    question_ids=[1, 3, 4],
                    exam_type="Timed",
                    duration=15,
                    created_at=datetime.now(),
                ),
                Exam(
                    title="Math & Science Practice",
                    categories=["Math", "Science"],
                    question_ids=[2, 5, 6],
                    exam_type="Untimed",
                    duration=0,
                    created_at=datetime.now(),
                ),
            ]
        q_state = await self.get_state(QuestionState)
        if not q_state.questions:
            q_state._add_sample_data()
        self.available_questions = q_state.questions

    @rx.var
    def filtered_questions_picker(self) -> list[Question]:
        """Filter questions in the picker."""
        if self.form_category_filter == "All":
            return self.available_questions
        return [
            q
            for q in self.available_questions
            if q.category == self.form_category_filter
        ]

    @rx.event
    def open_add_modal(self):
        self.is_editing = False
        self.form_title = ""
        self.form_duration = 30
        self.form_type = "Timed"
        self.form_selected_question_ids = []
        self.form_category_filter = "All"
        self.is_modal_open = True

    @rx.event
    def open_edit_modal(self, exam: Exam):
        self.is_editing = True
        try:
            self.current_exam_index = self.exams.index(exam)
        except ValueError as e:
            logging.exception(f"Error finding exam index: {e}")
            self.current_exam_index = -1
        self.form_title = exam.title
        self.form_duration = exam.duration
        self.form_type = exam.exam_type
        self.form_selected_question_ids = exam.question_ids
        self.form_category_filter = "All"
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False

    @rx.event
    def toggle_question_selection(self, q_id: int):
        if q_id in self.form_selected_question_ids:
            self.form_selected_question_ids.remove(q_id)
        else:
            self.form_selected_question_ids.append(q_id)

    @rx.event
    def save_exam(self):
        if not self.form_title:
            return rx.window_alert("Exam title is required")
        if not self.form_selected_question_ids:
            return rx.window_alert("Please select at least one question")
        selected_cats = set()
        for q in self.available_questions:
            if q.id in self.form_selected_question_ids:
                selected_cats.add(q.category)
        new_exam = Exam(
            title=self.form_title,
            categories=list(selected_cats),
            question_ids=self.form_selected_question_ids,
            exam_type=self.form_type,
            duration=self.form_duration if self.form_type == "Timed" else 0,
            created_at=datetime.now(),
        )
        if self.is_editing and self.current_exam_index != -1:
            self.exams[self.current_exam_index] = new_exam
        else:
            self.exams.insert(0, new_exam)
        self.is_modal_open = False
        rx.toast.success("Exam saved successfully")

    @rx.event
    def delete_exam(self, title: str):
        self.exams = [e for e in self.exams if e.title != title]