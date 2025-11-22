import reflex as rx
from app.components.sidebar import sidebar
from app.states.question_state import QuestionState
from app.models import Question


def question_form() -> rx.Component:
    """The form for creating or editing a question."""
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Question Text",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.textarea(
                placeholder="Enter the question here...",
                on_change=QuestionState.set_form_question_text,
                class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 min-h-[80px]",
                default_value=QuestionState.form_question_text,
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Type", class_name="block text-sm font-medium text-gray-700 mb-1"
                ),
                rx.el.select(
                    rx.el.option("MCQ", value="MCQ"),
                    rx.el.option("Short Answer", value="Short Answer"),
                    value=QuestionState.form_question_type,
                    on_change=QuestionState.set_form_question_type,
                    class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Category",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    list="categories-list",
                    placeholder="e.g. Math",
                    on_change=QuestionState.set_form_category,
                    class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500",
                    default_value=QuestionState.form_category,
                ),
                rx.el.datalist(
                    rx.foreach(
                        QuestionState.categories, lambda cat: rx.el.option(value=cat)
                    ),
                    id="categories-list",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Marks (1-5)",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.select(
                    rx.el.option("1", value="1"),
                    rx.el.option("2", value="2"),
                    rx.el.option("3", value="3"),
                    rx.el.option("4", value="4"),
                    rx.el.option("5", value="5"),
                    value=QuestionState.form_marks.to_string(),
                    on_change=lambda v: QuestionState.set_form_marks(v.to(int)),
                    class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500",
                ),
                class_name="w-24",
            ),
            class_name="flex gap-4 mb-4",
        ),
        rx.cond(
            QuestionState.form_question_type == "MCQ",
            rx.el.div(
                rx.el.label(
                    "Options & Correct Answer",
                    class_name="block text-sm font-medium text-gray-700 mb-2",
                ),
                rx.el.div(
                    rx.foreach(
                        QuestionState.form_mcq_options,
                        lambda opt, i: rx.el.div(
                            rx.el.input(
                                type="radio",
                                name="correct_answer",
                                checked=QuestionState.form_correct_answer == opt,
                                on_change=lambda _: QuestionState.set_form_correct_answer(
                                    opt
                                ),
                                class_name="mt-3 mr-2 w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500",
                            ),
                            rx.el.input(
                                placeholder=f"Option {i + 1}",
                                on_change=lambda v: QuestionState.update_mcq_option(
                                    i, v
                                ),
                                class_name="flex-1 px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500",
                                default_value=opt,
                            ),
                            class_name="flex items-start gap-2",
                        ),
                    ),
                    class_name="space-y-3",
                ),
                rx.el.p(
                    "Select the radio button next to the correct option text.",
                    class_name="text-xs text-gray-500 mt-2",
                ),
                class_name="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200",
            ),
            rx.el.div(
                rx.el.label(
                    "Answer Configuration",
                    class_name="block text-sm font-medium text-gray-700 mb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Correct Value (Whole Number)",
                            class_name="text-xs font-medium text-gray-500 uppercase",
                        ),
                        rx.el.input(
                            type="number",
                            placeholder="25",
                            on_change=QuestionState.set_form_short_answer_value,
                            class_name="w-full mt-1 px-4 py-2 rounded-lg border border-gray-300 focus:ring-teal-500",
                            default_value=QuestionState.form_short_answer_value,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Unit (e.g. kg, m)",
                            class_name="text-xs font-medium text-gray-500 uppercase",
                        ),
                        rx.el.input(
                            type="text",
                            placeholder="units",
                            on_change=QuestionState.set_form_unit,
                            class_name="w-full mt-1 px-4 py-2 rounded-lg border border-gray-300 focus:ring-teal-500",
                            default_value=QuestionState.form_unit,
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Tolerance (-)",
                            class_name="text-xs font-medium text-gray-500 uppercase",
                        ),
                        rx.el.input(
                            type="number",
                            min="0",
                            on_change=QuestionState.set_form_tolerance_min,
                            class_name="w-full mt-1 px-4 py-2 rounded-lg border border-gray-300 focus:ring-teal-500",
                            default_value=QuestionState.form_tolerance_min,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Tolerance (+)",
                            class_name="text-xs font-medium text-gray-500 uppercase",
                        ),
                        rx.el.input(
                            type="number",
                            min="0",
                            on_change=QuestionState.set_form_tolerance_max,
                            class_name="w-full mt-1 px-4 py-2 rounded-lg border border-gray-300 focus:ring-teal-500",
                            default_value=QuestionState.form_tolerance_max,
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4",
                ),
                rx.el.p(
                    "Example: If answer is 100 and tolerance is -5/+5, acceptable range is 95-105.",
                    class_name="text-xs text-gray-500 mt-2 italic",
                ),
                class_name="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200",
            ),
        ),
        rx.el.div(
            rx.el.label(
                "Feedback / Explanation",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.textarea(
                placeholder="Explanation shown to student after review...",
                on_change=QuestionState.set_form_feedback,
                class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 min-h-[80px]",
                default_value=QuestionState.form_feedback,
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.button(
                "Cancel",
                on_click=QuestionState.close_modal,
                class_name="px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium transition-colors",
            ),
            rx.el.button(
                rx.cond(QuestionState.is_editing, "Update Question", "Create Question"),
                on_click=QuestionState.save_question,
                class_name="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 font-medium shadow-sm transition-colors",
            ),
            class_name="flex justify-end gap-3 pt-4 border-t border-gray-100",
        ),
        class_name="flex flex-col h-full",
    )


def question_item(question: Question) -> rx.Component:
    """A single question item in the list."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        question.category,
                        class_name="inline-block px-2 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded-md mr-2",
                    ),
                    rx.el.span(
                        question.question_type,
                        class_name="inline-block px-2 py-1 text-xs font-medium bg-blue-50 text-blue-600 rounded-md mr-2",
                    ),
                    rx.el.span(
                        f"{question.marks} Marks",
                        class_name="inline-block px-2 py-1 text-xs font-medium bg-amber-50 text-amber-600 rounded-md",
                    ),
                    class_name="flex flex-wrap gap-1 mb-2",
                ),
                rx.el.h3(
                    question.question_text,
                    class_name="text-base font-medium text-gray-900 line-clamp-2",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=lambda: QuestionState.open_edit_modal(question),
                    class_name="p-2 text-gray-400 hover:text-teal-600 hover:bg-teal-50 rounded-lg transition-colors",
                    title="Edit",
                ),
                rx.el.button(
                    rx.icon("copy", class_name="w-4 h-4"),
                    on_click=lambda: QuestionState.duplicate_question(question.id),
                    class_name="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors",
                    title="Duplicate",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: QuestionState.delete_question(question.id),
                    class_name="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                    title="Delete",
                ),
                class_name="flex items-start gap-1 ml-4",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.cond(
                question.question_type == "MCQ",
                rx.el.div(
                    rx.el.span(
                        "Answer: ", class_name="text-xs font-semibold text-gray-500"
                    ),
                    rx.el.span(
                        question.correct_answer, class_name="text-sm text-gray-700"
                    ),
                ),
                rx.el.div(
                    rx.el.span(
                        "Answer: ", class_name="text-xs font-semibold text-gray-500"
                    ),
                    rx.el.span(
                        f"{question.correct_answer} {question.short_answer_config['unit']}",
                        class_name="text-sm text-gray-700",
                    ),
                ),
            ),
            class_name="mt-3 pt-3 border-t border-gray-50",
        ),
        class_name="bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all",
    )


def admin_questions_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Question Bank",
                            class_name="text-2xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            "Manage, search, and organize all assessment questions.",
                            class_name="text-gray-500 text-sm mt-1",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="w-5 h-5 mr-2"),
                        "Add New Question",
                        on_click=QuestionState.open_add_modal,
                        class_name="flex items-center px-4 py-2.5 bg-teal-600 text-white rounded-xl hover:bg-teal-700 font-semibold shadow-lg hover:shadow-xl transition-all",
                    ),
                    class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="w-5 h-5 text-gray-400 absolute left-3 top-2.5",
                        ),
                        rx.el.input(
                            placeholder="Search questions...",
                            on_change=QuestionState.set_search_keyword,
                            class_name="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-teal-500 outline-none",
                            default_value=QuestionState.search_keyword,
                        ),
                        class_name="relative flex-1 min-w-[200px]",
                    ),
                    rx.el.select(
                        rx.el.option("All Categories", value="All"),
                        rx.foreach(
                            QuestionState.categories,
                            lambda cat: rx.el.option(cat, value=cat),
                        ),
                        value=QuestionState.filter_category,
                        on_change=QuestionState.set_filter_category,
                        class_name="px-3 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-teal-500 bg-white",
                    ),
                    rx.el.select(
                        rx.el.option("All Types", value="All"),
                        rx.el.option("MCQ", value="MCQ"),
                        rx.el.option("Short Answer", value="Short Answer"),
                        value=QuestionState.filter_type,
                        on_change=QuestionState.set_filter_type,
                        class_name="px-3 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-teal-500 bg-white",
                    ),
                    rx.el.select(
                        rx.el.option("All Marks", value="All"),
                        rx.el.option("1 Mark", value="1"),
                        rx.el.option("2 Marks", value="2"),
                        rx.el.option("3 Marks", value="3"),
                        rx.el.option("4 Marks", value="4"),
                        rx.el.option("5 Marks", value="5"),
                        value=QuestionState.filter_marks,
                        on_change=QuestionState.set_filter_marks,
                        class_name="px-3 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-teal-500 bg-white",
                    ),
                    class_name="flex flex-col md:flex-row gap-3 mb-6",
                ),
                rx.cond(
                    QuestionState.filtered_questions.length() > 0,
                    rx.el.div(
                        rx.foreach(QuestionState.filtered_questions, question_item),
                        class_name="grid grid-cols-1 gap-4",
                    ),
                    rx.el.div(
                        rx.icon(
                            "file-search", class_name="w-12 h-12 text-gray-300 mb-3"
                        ),
                        rx.el.h3(
                            "No questions found", class_name="text-gray-900 font-medium"
                        ),
                        rx.el.p(
                            "Try adjusting your filters or search keywords.",
                            class_name="text-gray-500 text-sm",
                        ),
                        class_name="flex flex-col items-center justify-center py-12 bg-white rounded-xl border border-dashed border-gray-300",
                    ),
                ),
                class_name="p-6 max-w-7xl mx-auto w-full",
            ),
            rx.dialog.root(
                rx.dialog.content(
                    rx.el.div(
                        rx.el.h2(
                            rx.cond(
                                QuestionState.is_editing,
                                "Edit Question",
                                "Create New Question",
                            ),
                            class_name="text-xl font-bold text-gray-900 mb-4",
                        ),
                        question_form(),
                        class_name="bg-white rounded-xl shadow-2xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto",
                    )
                ),
                open=QuestionState.is_modal_open,
                on_open_change=QuestionState.set_is_modal_open,
            ),
            class_name="flex-1 bg-slate-50 overflow-y-auto",
            on_mount=QuestionState.on_mount,
        ),
        class_name="flex h-screen font-['Montserrat']",
    )