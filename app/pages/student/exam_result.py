import reflex as rx
from app.states.exam_session_state import ExamSessionState
from app.states.review_state import ReviewState
from app.states.grading_state import GradingState
from app.models import Question, Attempt


def result_question_card(question: Question, attempt: Attempt) -> rx.Component:
    user_ans = attempt.answers.get(question.id.to_string(), "Not Answered")
    correct_val = question.correct_answer.to(int)
    user_val = user_ans.to(int)
    tol_min = question.short_answer_config["tolerance_min"].to(int)
    tol_max = question.short_answer_config["tolerance_max"].to(int)
    unit = question.short_answer_config["unit"].to(str)
    is_mcq = question.question_type == "MCQ"
    is_short = question.question_type == "Short Answer"
    is_mcq_correct = user_ans == question.correct_answer
    is_short_correct = (user_val >= correct_val - tol_min) & (
        user_val <= correct_val + tol_max
    )
    is_correct = rx.cond(
        is_mcq, is_mcq_correct, rx.cond(is_short, is_short_correct, False)
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    f"Question",
                    class_name="text-xs font-bold text-gray-400 uppercase tracking-wider",
                ),
                rx.el.h3(
                    question.question_text,
                    class_name="text-lg font-medium text-gray-900 mt-1",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.cond(
                    is_correct,
                    rx.el.div(
                        rx.icon("check_check", class_name="w-6 h-6 text-green-500"),
                        rx.el.span(
                            f"+{question.marks}",
                            class_name="text-green-600 font-bold ml-2",
                        ),
                        class_name="flex items-center bg-green-50 px-3 py-1 rounded-full",
                    ),
                    rx.el.div(
                        rx.icon("circle_x", class_name="w-6 h-6 text-red-500"),
                        rx.el.span("0", class_name="text-red-600 font-bold ml-2"),
                        class_name="flex items-center bg-red-50 px-3 py-1 rounded-full",
                    ),
                ),
                class_name="ml-4",
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Your Answer", class_name="text-xs text-gray-500 mb-1"),
                rx.el.p(
                    rx.cond(is_short, user_ans + " " + unit, user_ans),
                    class_name=rx.cond(
                        is_correct,
                        "font-medium text-green-700",
                        "font-medium text-red-700",
                    ),
                ),
                class_name="flex-1 p-3 bg-gray-50 rounded-lg border border-gray-100",
            ),
            rx.el.div(
                rx.el.p("Correct Answer", class_name="text-xs text-gray-500 mb-1"),
                rx.el.p(
                    rx.cond(
                        is_short,
                        question.correct_answer + " " + unit,
                        question.correct_answer,
                    ),
                    class_name="font-medium text-gray-900",
                ),
                class_name="flex-1 p-3 bg-white border border-gray-200 rounded-lg ml-4",
            ),
            class_name="flex mb-4",
        ),
        rx.el.div(
            rx.el.span("Explanation: ", class_name="font-semibold text-gray-700"),
            rx.el.span(question.feedback, class_name="text-gray-600"),
            class_name="text-sm bg-blue-50 p-4 rounded-lg text-blue-800 border border-blue-100",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mb-4",
    )


def exam_result_page() -> rx.Component:
    last_attempt = rx.cond(
        GradingState.attempts,
        GradingState.attempts[-1],
        Attempt(student_id=0, exam_id=0, attempt_number=0, score=0),
    )
    review_enabled = ReviewState.settings.contains(ExamSessionState.exam_title)
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("trophy", class_name="w-16 h-16 text-yellow-400 mb-6"),
                rx.el.h1(
                    "Exam Completed!",
                    class_name="text-3xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    f"You have successfully submitted {ExamSessionState.exam_title}",
                    class_name="text-gray-500 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Your Score",
                            class_name="text-sm text-gray-500 uppercase tracking-wider font-medium",
                        ),
                        rx.el.h2(
                            f"{last_attempt.score}%",
                            class_name="text-5xl font-bold text-teal-600 mt-2",
                        ),
                        class_name="flex flex-col items-center p-6 bg-white rounded-2xl shadow-sm border border-gray-100 w-64",
                    ),
                    class_name="flex justify-center mb-12",
                ),
                rx.el.div(
                    rx.el.a(
                        rx.el.button(
                            "Return to Dashboard",
                            class_name="px-6 py-3 bg-gray-900 text-white rounded-xl hover:bg-gray-800 font-medium transition-colors",
                        ),
                        href="/student/dashboard",
                    ),
                    class_name="mb-12",
                ),
                rx.cond(
                    True,
                    rx.el.div(
                        rx.el.h3(
                            "Detailed Review",
                            class_name="text-xl font-bold text-gray-900 mb-6 text-left w-full max-w-3xl",
                        ),
                        rx.el.div(
                            rx.foreach(
                                ExamSessionState.questions,
                                lambda q: result_question_card(q, last_attempt),
                            ),
                            class_name="w-full max-w-3xl",
                        ),
                    ),
                    rx.el.p(
                        "Detailed review is not available for this exam.",
                        class_name="text-gray-500 italic",
                    ),
                ),
                class_name="flex flex-col items-center py-16 max-w-7xl mx-auto px-4",
            ),
            class_name="min-h-screen bg-slate-50 font-['Montserrat']",
        )
    )