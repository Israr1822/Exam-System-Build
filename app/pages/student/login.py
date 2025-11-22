import reflex as rx
from app.states.auth_state import AuthState


def student_login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("graduation-cap", class_name="w-12 h-12 text-teal-600"),
                class_name="mb-6 flex justify-center",
            ),
            rx.el.h1(
                "Student Login",
                class_name="text-2xl font-bold text-center text-gray-900 mb-2",
            ),
            rx.el.p(
                "Access your exams and results.",
                class_name="text-gray-500 text-center mb-8",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Email Address",
                        class_name="block text-sm font-medium text-gray-700 mb-2",
                    ),
                    rx.el.input(
                        name="email",
                        type="email",
                        placeholder="student@example.com",
                        required=True,
                        class_name="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all",
                    ),
                    class_name="mb-5",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password",
                        class_name="block text-sm font-medium text-gray-700 mb-2",
                    ),
                    rx.el.input(
                        name="password",
                        type="password",
                        placeholder="••••••••",
                        required=True,
                        class_name="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        AuthState.error_message,
                        class_name="mb-6 p-3 rounded-lg bg-red-50 text-red-600 text-sm border border-red-100",
                    ),
                    rx.el.div(),
                ),
                rx.el.button(
                    "Sign In",
                    type="submit",
                    class_name="w-full py-3 bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transition-all duration-200 mb-4",
                ),
                on_submit=AuthState.student_login,
            ),
            rx.el.div(
                rx.el.span("Don't have an account? ", class_name="text-gray-600"),
                rx.el.a(
                    "Register here",
                    href="/student/register",
                    class_name="text-teal-600 font-medium hover:underline",
                ),
                class_name="text-center text-sm",
            ),
            class_name="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100",
        ),
        class_name="min-h-screen flex items-center justify-center bg-slate-50 font-['Montserrat']",
    )