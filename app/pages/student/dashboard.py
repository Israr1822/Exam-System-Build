import reflex as rx
from app.states.auth_state import AuthState
from app.states.student_dashboard_state import StudentDashboardState


def exam_card(assignment: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                assignment["exam_title"],
                class_name="text-xl font-bold text-gray-900 mb-1",
            ),
            rx.el.div(
                rx.el.span(
                    assignment["exam_type"],
                    class_name=rx.cond(
                        assignment["exam_type"] == "Timed",
                        "bg-amber-100 text-amber-800 text-xs font-semibold px-2.5 py-0.5 rounded",
                        "bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded",
                    ),
                ),
                rx.el.span(
                    rx.cond(
                        assignment["exam_type"] == "Timed",
                        f"{assignment['duration']} mins",
                        "Untimed",
                    ),
                    class_name="text-gray-500 text-xs ml-2",
                ),
                class_name="flex items-center mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span("Attempts Left:", class_name="text-gray-500 text-sm"),
                    rx.el.span(
                        f" {assignment['attempts_left']}",
                        class_name="font-semibold text-gray-700 ml-1 text-sm",
                    ),
                    class_name="mb-1",
                ),
                rx.el.div(
                    rx.el.span("Expires:", class_name="text-gray-500 text-sm"),
                    rx.el.span(
                        f" {assignment['expiry_date']}",
                        class_name="font-semibold text-gray-700 ml-1 text-sm",
                    ),
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.cond(
                    assignment["status"] == "Available",
                    rx.el.button(
                        "Start Exam",
                        on_click=lambda: StudentDashboardState.start_exam(
                            assignment["exam_id"]
                        ),
                        class_name="w-full py-2 bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-lg transition-colors shadow-sm hover:shadow-md",
                    ),
                    rx.el.button(
                        assignment["status"],
                        disabled=True,
                        class_name="w-full py-2 bg-gray-100 text-gray-400 font-semibold rounded-lg cursor-not-allowed",
                    ),
                )
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:border-teal-200 transition-all",
    )


def student_dashboard_page() -> rx.Component:
    return rx.el.div(
        rx.el.nav(
            rx.el.div(
                rx.el.div(
                    rx.icon("graduation-cap", class_name="w-8 h-8 text-teal-600"),
                    rx.el.h1(
                        "Student Portal",
                        class_name="text-xl font-bold text-gray-900 ml-2",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.el.span(
                        AuthState.email, class_name="text-gray-600 mr-4 font-medium"
                    ),
                    rx.el.button(
                        "Logout",
                        on_click=AuthState.logout,
                        class_name="text-red-600 hover:text-red-800 font-medium text-sm",
                    ),
                    class_name="flex items-center",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between",
            ),
            class_name="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10",
        ),
        rx.el.main(
            rx.el.div(
                rx.el.h2(
                    "My Exams", class_name="text-2xl font-bold text-gray-900 mb-6"
                ),
                rx.cond(
                    StudentDashboardState.assignments_display.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            StudentDashboardState.assignments_display, exam_card
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                    rx.el.div(
                        rx.icon(
                            "calendar-x", class_name="w-12 h-12 text-gray-300 mb-4"
                        ),
                        rx.el.h3(
                            "No exams assigned",
                            class_name="text-lg font-medium text-gray-900 mb-1",
                        ),
                        rx.el.p(
                            "You don't have any pending exams at the moment.",
                            class_name="text-gray-500",
                        ),
                        class_name="flex flex-col items-center justify-center py-16 bg-white rounded-xl border border-dashed border-gray-300",
                    ),
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
            )
        ),
        class_name="min-h-screen bg-slate-50 font-['Montserrat']",
        on_mount=StudentDashboardState.on_load,
    )