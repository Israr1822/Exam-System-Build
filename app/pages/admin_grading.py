import reflex as rx
from app.components.sidebar import sidebar
from app.states.grading_state import GradingState
from app.models import Attempt


def attempt_card(attempt: Attempt) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    f"Student ID: {attempt.student_id}",
                    class_name="text-lg font-semibold text-gray-900",
                ),
                rx.el.p(
                    f"Exam ID: {attempt.exam_id} • Attempt #{attempt.attempt_number}",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        f"{attempt.score}%",
                        class_name="text-2xl font-bold text-teal-600",
                    ),
                    rx.el.p("Score", class_name="text-xs text-gray-400 text-right"),
                ),
                class_name="text-right ml-6",
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("clock", class_name="w-4 h-4 text-gray-400 mr-2"),
                rx.el.span(
                    f"{attempt.time_taken} seconds", class_name="text-sm text-gray-600"
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.icon("calendar", class_name="w-4 h-4 text-gray-400 mr-2"),
                rx.el.span(
                    attempt.submitted_at.to_string(), class_name="text-sm text-gray-600"
                ),
                class_name="flex items-center",
            ),
            class_name="flex gap-6 pt-4 border-t border-gray-100",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:border-teal-200 transition-colors",
    )


def admin_grading_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Grading & Results",
                    class_name="text-2xl font-bold text-gray-800 mb-2",
                ),
                rx.el.p(
                    "View student performance and attempt details.",
                    class_name="text-gray-500 mb-8",
                ),
                rx.el.div(
                    rx.foreach(GradingState.attempts, attempt_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                class_name="p-8 max-w-7xl mx-auto w-full",
            ),
            class_name="flex-1 bg-slate-50 overflow-y-auto",
            on_mount=GradingState.on_mount,
        ),
        class_name="flex h-screen font-['Montserrat']",
    )