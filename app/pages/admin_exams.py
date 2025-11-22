import reflex as rx
from app.components.sidebar import sidebar
from app.states.exam_state import ExamState
from app.states.student_state import StudentState
from app.states.assignment_state import AssignmentState
from app.models import Exam, Question


def question_picker_item(question: Question) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            rx.el.input(
                type="checkbox",
                checked=ExamState.form_selected_question_ids.contains(question.id),
                on_change=lambda _: ExamState.toggle_question_selection(question.id),
                class_name="w-5 h-5 text-teal-600 rounded border-gray-300 focus:ring-teal-500 mr-3",
            ),
            rx.el.div(
                rx.el.p(
                    question.question_text,
                    class_name="text-sm font-medium text-gray-900 line-clamp-1",
                ),
                rx.el.div(
                    rx.el.span(
                        f"{question.marks} Marks",
                        class_name="text-xs bg-gray-100 px-2 py-0.5 rounded text-gray-600 mr-2",
                    ),
                    rx.el.span(
                        question.category,
                        class_name="text-xs bg-blue-50 px-2 py-0.5 rounded text-blue-600",
                    ),
                    class_name="flex mt-1",
                ),
                class_name="flex-1",
            ),
            class_name="flex items-start p-3 hover:bg-gray-50 rounded-lg cursor-pointer border border-transparent hover:border-gray-200 transition-all",
        )
    )


def exam_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Exam Title",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    placeholder="Mid-term Assessment",
                    on_change=ExamState.set_form_title,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 mb-4",
                    default_value=ExamState.form_title,
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Exam Type",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Timed Exam", value="Timed"),
                            rx.el.option("Untimed Practice", value="Untimed"),
                            value=ExamState.form_type,
                            on_change=ExamState.set_form_type,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Duration (minutes)",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="number",
                            on_change=lambda v: ExamState.set_form_duration(v.to(int)),
                            disabled=ExamState.form_type == "Untimed",
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 disabled:bg-gray-100 disabled:text-gray-400",
                            default_value=ExamState.form_duration.to_string(),
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                class_name="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Select Questions", class_name="font-semibold text-gray-800"
                    ),
                    rx.el.select(
                        rx.el.option("All Categories", value="All"),
                        rx.el.option("Math", value="Math"),
                        rx.el.option("Science", value="Science"),
                        rx.el.option("History", value="History"),
                        rx.el.option("Geography", value="Geography"),
                        value=ExamState.form_category_filter,
                        on_change=ExamState.set_form_category_filter,
                        class_name="text-sm border-gray-300 rounded-md px-2 py-1",
                    ),
                    class_name="flex justify-between items-center mb-3",
                ),
                rx.el.div(
                    rx.foreach(
                        ExamState.filtered_questions_picker, question_picker_item
                    ),
                    class_name="h-64 overflow-y-auto border border-gray-200 rounded-lg p-2 bg-white space-y-1",
                ),
                rx.el.p(
                    f"Selected: {ExamState.form_selected_question_ids.length()} questions",
                    class_name="text-sm text-gray-500 mt-2 text-right",
                ),
            ),
        ),
        rx.el.div(
            rx.el.button(
                "Cancel",
                on_click=ExamState.close_modal,
                class_name="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg mr-2",
            ),
            rx.el.button(
                "Save Exam",
                on_click=ExamState.save_exam,
                class_name="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700",
            ),
            class_name="flex justify-end mt-6 pt-4 border-t border-gray-100",
        ),
    )


def assignment_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.h2("Assign Exam", class_name="text-xl font-bold mb-4"),
            rx.el.div(
                rx.el.p(
                    f"Assigning: {AssignmentState.selected_exam_title}",
                    class_name="text-sm text-teal-600 font-medium mb-4 bg-teal-50 p-2 rounded",
                ),
                rx.el.label(
                    "Select Student",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.select(
                    rx.el.option("Select a student...", value=""),
                    rx.foreach(
                        StudentState.students,
                        lambda s: rx.el.option(f"{s.name} ({s.email})", value=s.email),
                    ),
                    on_change=AssignmentState.set_selected_student_email,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Attempts Allowed",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="number",
                            min="1",
                            on_change=lambda v: AssignmentState.set_form_attempts(
                                v.to(int)
                            ),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500",
                            default_value=AssignmentState.form_attempts.to_string(),
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Expires In (Days)",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="number",
                            min="1",
                            on_change=lambda v: AssignmentState.set_form_expiry_days(
                                v.to(int)
                            ),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500",
                            default_value=AssignmentState.form_expiry_days.to_string(),
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=AssignmentState.close_modal,
                        class_name="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg mr-2",
                    ),
                    rx.el.button(
                        "Assign Exam",
                        on_click=AssignmentState.create_assignment,
                        class_name="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700",
                    ),
                    class_name="flex justify-end",
                ),
            ),
            class_name="bg-white p-6 rounded-xl shadow-xl w-full max-w-md",
        ),
        open=AssignmentState.is_modal_open,
        on_open_change=AssignmentState.set_is_modal_open,
    )


def exam_row(exam: Exam) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(exam.title, class_name="text-sm font-medium text-gray-900"),
                rx.el.div(
                    rx.foreach(
                        exam.categories,
                        lambda c: rx.el.span(
                            c,
                            class_name="text-xs text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded mr-1",
                        ),
                    ),
                    class_name="mt-1",
                ),
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(
                exam.exam_type,
                class_name=rx.cond(
                    exam.exam_type == "Timed",
                    "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-amber-100 text-amber-800",
                    "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(exam.exam_type == "Timed", f"{exam.duration} mins", "Unlimited"),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            f"{exam.question_ids.length()} Qs",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("user-plus", class_name="w-4 h-4"),
                    on_click=lambda: AssignmentState.open_assign_modal(exam.title),
                    class_name="text-blue-600 hover:text-blue-900 p-2 hover:bg-blue-50 rounded-lg transition-colors mr-1",
                    title="Assign to Student",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=lambda: ExamState.open_edit_modal(exam),
                    class_name="text-teal-600 hover:text-teal-900 p-2 hover:bg-teal-50 rounded-lg transition-colors mr-1",
                    title="Edit Exam",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: ExamState.delete_exam(exam.title),
                    class_name="text-red-600 hover:text-red-900 p-2 hover:bg-red-50 rounded-lg transition-colors",
                    title="Delete Exam",
                ),
                class_name="flex justify-end",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100",
    )


def admin_exams_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Exam Management",
                            class_name="text-2xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            "Create exams and assign them to students.",
                            class_name="text-gray-500 text-sm mt-1",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="w-5 h-5 mr-2"),
                        "Create Exam",
                        on_click=ExamState.open_add_modal,
                        class_name="flex items-center px-4 py-2 bg-teal-600 text-white rounded-xl hover:bg-teal-700 font-semibold shadow-sm transition-all",
                    ),
                    class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Exam Title",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Type",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Duration",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Questions",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Actions",
                                    class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                            ),
                            class_name="bg-gray-50",
                        ),
                        rx.el.tbody(
                            rx.foreach(ExamState.exams, exam_row),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden",
                ),
                class_name="p-8 max-w-7xl mx-auto w-full",
            ),
            rx.dialog.root(
                rx.dialog.content(
                    rx.el.h2(
                        rx.cond(ExamState.is_editing, "Edit Exam", "Create New Exam"),
                        class_name="text-xl font-bold mb-4",
                    ),
                    exam_form(),
                    class_name="bg-white p-6 rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto",
                ),
                open=ExamState.is_modal_open,
                on_open_change=ExamState.set_is_modal_open,
            ),
            assignment_modal(),
            class_name="flex-1 bg-slate-50 overflow-y-auto",
            on_mount=[
                ExamState.on_mount,
                StudentState.on_mount,
                AssignmentState.on_mount,
            ],
        ),
        class_name="flex h-screen font-['Montserrat']",
    )