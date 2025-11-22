import reflex as rx
from app.components.sidebar import sidebar
from app.states.student_state import StudentState
from app.models import Student


def student_row(student: Student) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "user",
                        class_name="w-8 h-8 text-teal-600 bg-teal-50 rounded-full p-1.5",
                    ),
                    rx.el.div(
                        rx.el.p(
                            student.name, class_name="text-sm font-medium text-gray-900"
                        ),
                        rx.el.p(student.email, class_name="text-xs text-gray-500"),
                        class_name="ml-3",
                    ),
                    class_name="flex items-center",
                )
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                "Active",
                class_name="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            student.created_at.to_string(),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.button(
                rx.icon("trash-2", class_name="w-4 h-4"),
                on_click=lambda: StudentState.delete_student(student.email),
                class_name="text-red-600 hover:text-red-900 p-2 hover:bg-red-50 rounded-lg transition-colors",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100",
    )


def admin_students_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Student Management",
                            class_name="text-2xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            "Manage registered students and their accounts.",
                            class_name="text-gray-500 text-sm mt-1",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="w-5 h-5 mr-2"),
                        "Add Student",
                        on_click=StudentState.open_add_modal,
                        class_name="flex items-center px-4 py-2 bg-teal-600 text-white rounded-xl hover:bg-teal-700 font-semibold shadow-sm transition-all",
                    ),
                    class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
                ),
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-3 w-5 h-5 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Search by name or email...",
                        on_change=StudentState.set_search_query,
                        class_name="pl-10 pr-4 py-2 w-full md:w-96 rounded-lg border border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none",
                        default_value=StudentState.search_query,
                    ),
                    class_name="relative mb-6",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Student",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Joined Date",
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
                            rx.foreach(StudentState.filtered_students, student_row),
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
                    rx.el.h2("Add New Student", class_name="text-xl font-bold mb-4"),
                    rx.el.div(
                        rx.el.label(
                            "Full Name",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="John Doe",
                            on_change=StudentState.set_form_name,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 mb-4",
                        ),
                        rx.el.label(
                            "Email Address",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="email",
                            placeholder="john@example.com",
                            on_change=StudentState.set_form_email,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 mb-4",
                        ),
                        rx.el.label(
                            "Password",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="password",
                            placeholder="******",
                            on_change=StudentState.set_form_password,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500 mb-6",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Cancel",
                                on_click=StudentState.close_modal,
                                class_name="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg mr-2",
                            ),
                            rx.el.button(
                                "Add Student",
                                on_click=StudentState.save_student,
                                class_name="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700",
                            ),
                            class_name="flex justify-end",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-xl w-full max-w-md",
                ),
                open=StudentState.is_modal_open,
                on_open_change=StudentState.set_is_modal_open,
            ),
            class_name="flex-1 bg-slate-50 overflow-y-auto",
            on_mount=StudentState.on_mount,
        ),
        class_name="flex h-screen font-['Montserrat']",
    )