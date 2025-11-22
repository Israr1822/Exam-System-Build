import reflex as rx
from app.states.exam_session_state import ExamSessionState
from app.models import Question


def question_sidebar_item(idx: int, question: Question) -> rx.Component:
    is_current = ExamSessionState.current_question_index == idx
    is_answered = ExamSessionState.answers.contains(question.id)
    is_bookmarked = ExamSessionState.bookmarks.contains(question.id)
    base_style = "flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium cursor-pointer transition-colors mb-1 "
    return rx.el.div(
        rx.el.div(
            rx.el.span(f"{idx + 1}. ", class_name="mr-1 opacity-70"),
            rx.el.span(f"Question {idx + 1}"),
            rx.el.span(f"({question.marks})", class_name="ml-2 text-xs opacity-60"),
            class_name="flex items-center",
        ),
        rx.cond(
            is_bookmarked,
            rx.icon("bookmark", class_name="w-3 h-3 fill-current"),
            rx.el.span(),
        ),
        class_name=rx.cond(
            is_current,
            base_style + "bg-teal-600 text-white shadow-md",
            rx.cond(
                is_answered,
                base_style + "bg-blue-50 text-blue-700 border border-blue-100",
                base_style
                + "bg-gray-50 text-gray-600 hover:bg-gray-100 border border-transparent",
            ),
        ),
        on_click=lambda: ExamSessionState.jump_to_question(idx),
    )


def mcq_option(option: str) -> rx.Component:
    return rx.el.label(
        rx.el.input(
            type="radio",
            name="mcq_answer",
            value=option,
            checked=ExamSessionState.answers[
                ExamSessionState.current_question.id.to_string()
            ]
            == option,
            on_change=lambda _: ExamSessionState.set_answer(option),
            class_name="w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500 mr-3",
        ),
        rx.el.span(option, class_name="text-gray-700"),
        class_name="flex items-center p-4 border border-gray-200 rounded-xl hover:bg-gray-50 cursor-pointer transition-colors bg-white",
    )


def exam_session_page() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.h1(
                    ExamSessionState.exam_title,
                    class_name="text-lg font-bold text-gray-900",
                ),
                rx.el.div(
                    rx.cond(
                        ExamSessionState.is_timed,
                        rx.el.div(
                            rx.icon("clock", class_name="w-5 h-5 text-teal-600 mr-2"),
                            rx.el.span(
                                ExamSessionState.formatted_time,
                                class_name="font-mono text-xl font-bold text-teal-700",
                            ),
                            class_name="flex items-center bg-teal-50 px-4 py-2 rounded-lg border border-teal-100",
                        ),
                    ),
                    rx.el.button(
                        "Submit Exam",
                        on_click=ExamSessionState.open_submit_modal,
                        class_name="ml-4 px-6 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 font-medium transition-colors",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-center h-full",
            ),
            class_name="h-20 bg-white border-b border-gray-200 px-8 fixed top-0 w-full z-20",
        ),
        rx.el.div(
            rx.el.aside(
                rx.el.div(
                    rx.el.h3(
                        "Questions",
                        class_name="font-bold text-gray-400 uppercase text-xs mb-4 tracking-wider",
                    ),
                    rx.el.div(
                        rx.foreach(
                            ExamSessionState.questions,
                            lambda q, i: question_sidebar_item(i, q),
                        ),
                        class_name="space-y-1 overflow-y-auto max-h-[calc(100vh-140px)] pr-2",
                    ),
                    rx.el.div(
                        rx.el.div(
                            class_name="h-full bg-teal-500 transition-all duration-500",
                            style={"width": f"{ExamSessionState.progress_percentage}%"},
                        ),
                        class_name="h-1 w-full bg-gray-100 rounded-full overflow-hidden mt-6",
                    ),
                    rx.el.p(
                        f"{ExamSessionState.progress_percentage}% Completed",
                        class_name="text-xs text-gray-400 mt-2 text-center",
                    ),
                    class_name="p-6 h-full",
                ),
                class_name="w-72 h-[calc(100vh-80px)] fixed top-20 left-0 bg-white border-r border-gray-200 hidden md:block",
            ),
            rx.el.main(
                rx.cond(
                    ExamSessionState.current_question,
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    f"Question {ExamSessionState.current_question_index + 1}",
                                    class_name="text-sm font-bold text-teal-600 bg-teal-50 px-3 py-1 rounded-full uppercase tracking-wide",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        f"{ExamSessionState.current_question.marks} Marks",
                                        class_name="text-sm text-gray-500 mr-4",
                                    ),
                                    rx.el.button(
                                        rx.icon(
                                            "bookmark",
                                            class_name=rx.cond(
                                                ExamSessionState.bookmarks.contains(
                                                    ExamSessionState.current_question.id
                                                ),
                                                "w-5 h-5 text-amber-400 fill-current",
                                                "w-5 h-5 text-gray-300 hover:text-gray-500",
                                            ),
                                        ),
                                        on_click=ExamSessionState.toggle_bookmark,
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="flex justify-between items-center mb-6",
                            ),
                            rx.el.h2(
                                ExamSessionState.current_question.question_text,
                                class_name="text-2xl font-medium text-gray-900 mb-8 leading-relaxed",
                            ),
                            rx.el.div(
                                rx.cond(
                                    ExamSessionState.current_question.question_type
                                    == "MCQ",
                                    rx.el.div(
                                        rx.foreach(
                                            ExamSessionState.current_question.mcq_options,
                                            mcq_option,
                                        ),
                                        class_name="grid grid-cols-1 gap-3 max-w-2xl",
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "Your Answer:",
                                            class_name="block text-sm font-medium text-gray-700 mb-2",
                                        ),
                                        rx.el.div(
                                            rx.el.input(
                                                type="number",
                                                placeholder="Enter a whole number...",
                                                on_change=ExamSessionState.set_answer,
                                                class_name="flex-1 px-4 py-3 rounded-l-xl border border-gray-300 focus:ring-2 focus:ring-teal-500 outline-none text-lg",
                                                default_value=ExamSessionState.answers[
                                                    ExamSessionState.current_question.id.to_string()
                                                ],
                                            ),
                                            rx.el.div(
                                                ExamSessionState.current_question.short_answer_config[
                                                    "unit"
                                                ],
                                                class_name="bg-gray-50 border-y border-r border-gray-300 px-4 py-3 rounded-r-xl text-gray-500 font-medium flex items-center",
                                            ),
                                            class_name="flex max-w-md shadow-sm",
                                        ),
                                    ),
                                ),
                                class_name="mb-12",
                            ),
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("chevron-left", class_name="w-5 h-5 mr-1"),
                                "Previous",
                                on_click=ExamSessionState.prev_question,
                                disabled=ExamSessionState.current_question_index == 0,
                                class_name="flex items-center px-6 py-3 rounded-xl border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors",
                            ),
                            rx.el.button(
                                "Next",
                                rx.icon("chevron-right", class_name="w-5 h-5 ml-1"),
                                on_click=ExamSessionState.next_question,
                                disabled=ExamSessionState.current_question_index
                                == ExamSessionState.questions.length() - 1,
                                class_name="flex items-center px-6 py-3 bg-teal-600 text-white rounded-xl hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-lg shadow-teal-200",
                            ),
                            class_name="flex justify-between pt-8 border-t border-gray-100",
                        ),
                        class_name="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 min-h-[600px] flex flex-col justify-between",
                    ),
                    rx.el.div(
                        "Loading question...",
                        class_name="p-8 text-center text-gray-500",
                    ),
                ),
                class_name="md:ml-72 mt-20 p-8 max-w-5xl mx-auto",
            ),
            class_name="min-h-screen bg-slate-50 font-['Montserrat']",
        ),
        rx.dialog.root(
            rx.dialog.content(
                rx.el.h2("Submit Exam?", class_name="text-xl font-bold mb-4"),
                rx.el.p(
                    "Are you sure you want to submit? You will not be able to change your answers after submission.",
                    class_name="text-gray-600 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=ExamSessionState.close_submit_modal,
                        class_name="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg mr-2",
                    ),
                    rx.el.button(
                        "Confirm Submit",
                        on_click=ExamSessionState.submit_exam,
                        class_name="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700",
                    ),
                    class_name="flex justify-end",
                ),
                class_name="bg-white p-6 rounded-xl shadow-xl max-w-md w-full",
            ),
            open=ExamSessionState.confirm_submit_open,
            on_open_change=ExamSessionState.close_submit_modal,
        ),
        on_mount=ExamSessionState.load_exam,
    )