import reflex as rx
from app.pages.admin_login import admin_login_page
from app.pages.admin_dashboard import admin_dashboard_page
from app.pages.admin_questions import admin_questions_page
from app.pages.admin_exams import admin_exams_page
from app.pages.admin_students import admin_students_page
from app.pages.admin_review import admin_review_page
from app.pages.admin_grading import admin_grading_page
from app.pages.student.login import student_login_page
from app.pages.student.dashboard import student_dashboard_page
from app.states.auth_state import AuthState


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("graduation-cap", class_name="w-16 h-16 text-teal-600 mb-6"),
            rx.el.h1(
                "Exam Management System",
                class_name="text-4xl font-bold text-gray-900 mb-4 text-center",
            ),
            rx.el.p(
                "Secure, robust, and easy to use assessment platform.",
                class_name="text-xl text-gray-600 mb-12 text-center max-w-lg",
            ),
            rx.el.div(
                rx.el.a(
                    rx.el.button(
                        "Admin Portal",
                        rx.icon("shield-check", class_name="w-5 h-5 ml-2"),
                        class_name="flex items-center px-8 py-4 bg-teal-600 text-white rounded-xl hover:bg-teal-700 transition-all font-semibold shadow-lg hover:shadow-xl",
                    ),
                    href="/admin/login",
                ),
                rx.el.a(
                    rx.el.button(
                        "Student Portal",
                        rx.icon("user", class_name="w-5 h-5 ml-2"),
                        class_name="flex items-center px-8 py-4 bg-white text-teal-700 border-2 border-teal-600 rounded-xl hover:bg-teal-50 transition-all font-semibold shadow-lg hover:shadow-xl",
                    ),
                    href="/student/login",
                ),
                class_name="flex gap-6",
            ),
            class_name="flex flex-col items-center justify-center min-h-screen max-w-7xl mx-auto px-4",
        ),
        class_name="min-h-screen bg-slate-50 font-['Montserrat']",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="teal", radius="large"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(admin_login_page, route="/admin/login")
app.add_page(
    admin_dashboard_page, route="/admin/dashboard", on_load=AuthState.on_load_admin
)
app.add_page(
    admin_questions_page, route="/admin/questions", on_load=AuthState.on_load_admin
)
app.add_page(admin_exams_page, route="/admin/exams", on_load=AuthState.on_load_admin)
app.add_page(
    admin_students_page, route="/admin/students", on_load=AuthState.on_load_admin
)
app.add_page(admin_review_page, route="/admin/review", on_load=AuthState.on_load_admin)
app.add_page(
    admin_grading_page, route="/admin/grading", on_load=AuthState.on_load_admin
)
from app.pages.student.register import student_register_page
from app.pages.student.exam_session import exam_session_page
from app.pages.student.exam_result import exam_result_page

app.add_page(student_login_page, route="/student/login")
app.add_page(student_register_page, route="/student/register")
app.add_page(
    student_dashboard_page,
    route="/student/dashboard",
    on_load=AuthState.on_load_student,
)
app.add_page(
    exam_session_page, route="/student/exam/[e_id]", on_load=AuthState.on_load_student
)
app.add_page(
    exam_result_page,
    route="/student/exam/[e_id]/result",
    on_load=AuthState.on_load_student,
)