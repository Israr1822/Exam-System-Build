import reflex as rx
from app.states.auth_state import AuthState


def sidebar_item(text: str, icon_name: str, href: str) -> rx.Component:
    """A single sidebar navigation item."""
    return rx.el.a(
        rx.el.div(
            rx.icon(icon_name, class_name="w-5 h-5"),
            rx.el.span(text, class_name="font-medium"),
            class_name="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-teal-800 hover:text-white rounded-lg transition-colors duration-200",
        ),
        href=href,
        class_name="w-full",
    )


def sidebar() -> rx.Component:
    """The admin sidebar component."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("graduation-cap", class_name="w-8 h-8 text-teal-400"),
                rx.el.h1(
                    "ExamMaster",
                    class_name="text-xl font-bold text-white tracking-wide",
                ),
                class_name="flex items-center gap-3 px-6 py-6 border-b border-teal-800/50",
            ),
            rx.el.nav(
                sidebar_item("Dashboard", "layout-dashboard", "/admin/dashboard"),
                sidebar_item("Questions", "file-question", "/admin/questions"),
                sidebar_item("Exams", "scroll-text", "/admin/exams"),
                sidebar_item("Students", "users", "/admin/students"),
                sidebar_item("Review Settings", "settings-2", "/admin/review"),
                sidebar_item("Grading", "square_check", "/admin/grading"),
                class_name="flex flex-col gap-1 p-4 flex-1",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("log-out", class_name="w-5 h-5"),
                    rx.el.span("Logout", class_name="font-medium"),
                    on_click=AuthState.logout,
                    class_name="flex items-center gap-3 px-4 py-3 text-red-300 hover:bg-red-900/30 hover:text-red-100 rounded-lg transition-colors duration-200 w-full text-left",
                ),
                class_name="p-4 border-t border-teal-800/50",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="w-64 h-screen bg-slate-900 text-white sticky top-0 hidden md:block shadow-xl flex-shrink-0",
    )