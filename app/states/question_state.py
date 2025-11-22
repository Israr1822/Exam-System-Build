import reflex as rx
import logging
from app.models import Question
from typing import Any


class QuestionState(rx.State):
    """State for managing questions."""

    questions: list[Question] = []
    next_id: int = 1
    search_keyword: str = ""
    filter_category: str = "All"
    filter_type: str = "All"
    filter_marks: str = "All"
    is_modal_open: bool = False
    is_editing: bool = False
    current_question_id: int = 0
    form_question_text: str = ""
    form_question_type: str = "MCQ"
    form_category: str = ""
    form_marks: int = 1
    form_feedback: str = ""
    form_mcq_options: list[str] = ["", "", "", ""]
    form_correct_answer: str = ""
    form_short_answer_value: str = ""
    form_tolerance_min: str = "0"
    form_tolerance_max: str = "0"
    form_unit: str = ""
    categories: list[str] = ["Math", "Science", "History", "Geography", "Programming"]

    @rx.event
    def on_mount(self):
        """Initialize with sample data if empty."""
        if not self.questions:
            self._add_sample_data()

    def _add_sample_data(self):
        """Populate with dummy data for testing."""
        sample_questions = [
            Question(
                id=self.next_id,
                question_text="What is the capital of France?",
                question_type="MCQ",
                category="Geography",
                marks=1,
                feedback="Paris is the capital and most populous city of France.",
                mcq_options=["London", "Berlin", "Paris", "Madrid"],
                correct_answer="Paris",
            ),
            Question(
                id=self.next_id + 1,
                question_text="Calculate the area of a square with side 5m.",
                question_type="Short Answer",
                category="Math",
                marks=2,
                feedback="Area = side * side = 5 * 5 = 25",
                correct_answer="25",
                short_answer_config={
                    "tolerance_min": 0,
                    "tolerance_max": 0,
                    "unit": "m²",
                },
            ),
            Question(
                id=self.next_id + 2,
                question_text="Which planet is known as the Red Planet?",
                question_type="MCQ",
                category="Science",
                marks=1,
                feedback="Mars appears red due to iron oxide on its surface.",
                mcq_options=["Venus", "Mars", "Jupiter", "Saturn"],
                correct_answer="Mars",
            ),
            Question(
                id=self.next_id + 3,
                question_text="Who wrote 'Romeo and Juliet'?",
                question_type="MCQ",
                category="History",
                marks=1,
                feedback="William Shakespeare wrote the play early in his career.",
                mcq_options=[
                    "Charles Dickens",
                    "Jane Austen",
                    "William Shakespeare",
                    "Mark Twain",
                ],
                correct_answer="William Shakespeare",
            ),
            Question(
                id=self.next_id + 4,
                question_text="Convert 100 degrees Celsius to Fahrenheit.",
                question_type="Short Answer",
                category="Science",
                marks=3,
                feedback="(100 × 9/5) + 32 = 212",
                correct_answer="212",
                short_answer_config={
                    "tolerance_min": 1,
                    "tolerance_max": 1,
                    "unit": "°F",
                },
            ),
            Question(
                id=self.next_id + 5,
                question_text="What is the chemical symbol for Gold?",
                question_type="MCQ",
                category="Science",
                marks=2,
                feedback="Au comes from the Latin word for gold, Aurum.",
                mcq_options=["Ag", "Au", "Fe", "Cu"],
                correct_answer="Au",
            ),
        ]
        self.questions = sample_questions
        self.next_id += 6

    @rx.var
    def filtered_questions(self) -> list[Question]:
        """Filter questions based on search and filter criteria."""
        filtered = self.questions
        if self.search_keyword:
            keyword = self.search_keyword.lower()
            filtered = [
                q
                for q in filtered
                if keyword in q.question_text.lower() or keyword in q.category.lower()
            ]
        if self.filter_category != "All":
            filtered = [q for q in filtered if q.category == self.filter_category]
        if self.filter_type != "All":
            filtered = [q for q in filtered if q.question_type == self.filter_type]
        if self.filter_marks != "All":
            try:
                marks = int(self.filter_marks)
                filtered = [q for q in filtered if q.marks == marks]
            except ValueError as e:
                logging.exception(f"Error filtering marks: {e}")
        return filtered

    @rx.event
    def open_add_modal(self):
        """Open modal to add a new question."""
        self.is_editing = False
        self.current_question_id = 0
        self.form_question_text = ""
        self.form_question_type = "MCQ"
        self.form_category = ""
        self.form_marks = 1
        self.form_feedback = ""
        self.form_mcq_options = ["", "", "", ""]
        self.form_correct_answer = ""
        self.form_short_answer_value = ""
        self.form_tolerance_min = "0"
        self.form_tolerance_max = "0"
        self.form_unit = ""
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        """Close the modal."""
        self.is_modal_open = False

    @rx.event
    def open_edit_modal(self, question: Question):
        """Open modal to edit an existing question."""
        self.is_editing = True
        self.current_question_id = question.id
        self.form_question_text = question.question_text
        self.form_question_type = question.question_type
        self.form_category = question.category
        self.form_marks = question.marks
        self.form_feedback = question.feedback
        if question.question_type == "MCQ":
            self.form_mcq_options = question.mcq_options.copy()
            while len(self.form_mcq_options) < 4:
                self.form_mcq_options.append("")
            self.form_correct_answer = question.correct_answer
            self.form_short_answer_value = ""
            self.form_tolerance_min = "0"
            self.form_tolerance_max = "0"
            self.form_unit = ""
        else:
            self.form_correct_answer = question.correct_answer
            self.form_short_answer_value = question.correct_answer
            self.form_tolerance_min = str(
                question.short_answer_config.get("tolerance_min", "0")
            )
            self.form_tolerance_max = str(
                question.short_answer_config.get("tolerance_max", "0")
            )
            self.form_unit = str(question.short_answer_config.get("unit", ""))
            self.form_mcq_options = ["", "", "", ""]
        self.is_modal_open = True

    @rx.event
    def update_mcq_option(self, index: int, value: str):
        """Update a specific MCQ option."""
        self.form_mcq_options[index] = value

    @rx.event
    def save_question(self):
        """Save the question (create or update)."""
        if not self.form_question_text.strip():
            return rx.window_alert("Question text is required.")
        if not self.form_category.strip():
            return rx.window_alert("Category is required.")
        new_question = Question(
            id=self.current_question_id if self.is_editing else self.next_id,
            question_text=self.form_question_text,
            question_type=self.form_question_type,
            category=self.form_category,
            marks=self.form_marks,
            feedback=self.form_feedback,
        )
        if self.form_question_type == "MCQ":
            valid_options = [opt for opt in self.form_mcq_options if opt.strip()]
            if len(valid_options) < 2:
                return rx.window_alert("Please provide at least 2 valid options.")
            if not self.form_correct_answer:
                return rx.window_alert("Please select a correct answer.")
            if self.form_correct_answer not in self.form_mcq_options:
                pass
            new_question.mcq_options = self.form_mcq_options
            new_question.correct_answer = self.form_correct_answer
        else:
            if not self.form_short_answer_value.strip():
                return rx.window_alert("Correct answer value is required.")
            try:
                val = int(self.form_short_answer_value)
            except ValueError as e:
                logging.exception(f"Error parsing short answer value: {e}")
                return rx.window_alert("Short answer must be a whole number.")
            new_question.correct_answer = str(val)
            new_question.short_answer_config = {
                "tolerance_min": int(self.form_tolerance_min or 0),
                "tolerance_max": int(self.form_tolerance_max or 0),
                "unit": self.form_unit,
            }
        if self.is_editing:
            for i, q in enumerate(self.questions):
                if q.id == self.current_question_id:
                    self.questions[i] = new_question
                    break
        else:
            self.questions.append(new_question)
            self.next_id += 1
        self.is_modal_open = False

    @rx.event
    def delete_question(self, question_id: int):
        """Delete a question."""
        self.questions = [q for q in self.questions if q.id != question_id]

    @rx.event
    def duplicate_question(self, question_id: int):
        """Duplicate a question."""
        for q in self.questions:
            if q.id == question_id:
                new_q = q.copy()
                new_q.id = self.next_id
                new_q.question_text = f"{q.question_text} (Copy)"
                self.questions.append(new_q)
                self.next_id += 1
                break