import reflex as rx
from app.components.sidebar import sidebar
from app.states.exam_state import ExamState
from app.states.review_state import ReviewState
from app.models import Exam


def review_settings_row(exam: Exam) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(exam.title, class_name="text-lg font-semibold text-gray-900"),
            rx.el.p(
                f"{exam.question_ids.length()} Questions • {exam.duration} mins",
                class_name="text-sm text-gray-500",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Review Access",
                    class_name="text-xs font-bold text-gray-500 uppercase mb-1 block",
                ),
                rx.el.button(
                    rx.cond(
                        ReviewState.settings[exam.title].review_enabled,
                        rx.el.span("Enabled", class_name="text-green-600 font-medium"),
                        rx.el.span("Disabled", class_name="text-red-500 font-medium"),
                    ),
                    on_click=lambda: ReviewState.toggle_review(exam.title),
                    class_name="bg-gray-100 px-3 py-1.5 rounded-lg border border-gray-200 hover:bg-gray-200 transition-colors w-24",
                ),
                class_name="mr-6",
            ),
            rx.el.div(
                rx.el.label(
                    "Exam Mode",
                    class_name="text-xs font-bold text-gray-500 uppercase mb-1 block",
                ),
                rx.el.select(
                    rx.el.option("Assessment", value="Assessment"),
                    rx.el.option("Practice", value="Practice"),
                    value=ReviewState.settings[exam.title].exam_mode.to_string(),
                    on_change=lambda v: ReviewState.set_mode(exam.title, v),
                    class_name="bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-teal-500 focus:border-teal-500 block p-1.5",
                ),
            ),
            class_name="flex items-center",
        ),
        class_name="flex items-center justify-between p-6 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow",
    )


def admin_review_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Review & Access Settings",
                    class_name="text-2xl font-bold text-gray-800 mb-2",
                ),
                rx.el.p(
                    "Control how students access reviews and exam modes.",
                    class_name="text-gray-500 mb-8",
                ),
                rx.el.div(
                    rx.foreach(ExamState.exams, review_settings_row),
                    class_name="space-y-4",
                ),
                class_name="p-8 max-w-7xl mx-auto w-full",
            ),
            class_name="flex-1 bg-slate-50 overflow-y-auto",
            on_mount=[ExamState.on_mount, ReviewState.on_mount],
        ),
        class_name="flex h-screen font-['Montserrat']",
    )