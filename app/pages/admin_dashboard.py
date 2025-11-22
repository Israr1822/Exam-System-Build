import reflex as rx
from app.components.sidebar import sidebar
from app.states.auth_state import AuthState


def stat_card(title: str, value: str, icon: str, color_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500 mb-1"),
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.icon(icon, class_name=f"w-6 h-6 {color_class}"),
            class_name="p-3 bg-gray-50 rounded-lg",
        ),
        class_name="flex items-start bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow",
    )


def quick_action_card(title: str, desc: str, icon: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="w-8 h-8 text-teal-600 mb-4"),
            rx.el.h3(title, class_name="text-lg font-semibold text-gray-900 mb-2"),
            rx.el.p(desc, class_name="text-sm text-gray-500"),
            class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:border-teal-200 hover:shadow-md transition-all group",
        ),
        href=href,
        class_name="block",
    )


def admin_dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Dashboard Overview",
                        class_name="text-2xl font-bold text-gray-800",
                    ),
                    rx.el.p("Welcome back, Admin", class_name="text-gray-500 mt-1"),
                    class_name="mb-8",
                ),
                rx.el.div(
                    stat_card("Total Students", "1,234", "users", "text-blue-600"),
                    stat_card("Active Exams", "12", "scroll-text", "text-teal-600"),
                    stat_card(
                        "Questions Bank", "540", "file-question", "text-purple-600"
                    ),
                    stat_card("Pending Reviews", "8", "badge_alert", "text-orange-600"),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10",
                ),
                rx.el.h2(
                    "Quick Actions", class_name="text-lg font-bold text-gray-800 mb-4"
                ),
                rx.el.div(
                    quick_action_card(
                        "Create New Exam",
                        "Set up a new assessment or practice test",
                        "circle_plus",
                        "/admin/exams",
                    ),
                    quick_action_card(
                        "Add Questions",
                        "Expand the question bank with new items",
                        "file-plus",
                        "/admin/questions",
                    ),
                    quick_action_card(
                        "Assign Students",
                        "Enroll students to existing exams",
                        "user-plus",
                        "/admin/students",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                ),
                class_name="p-8 max-w-7xl mx-auto w-full",
            ),
            class_name="flex-1 bg-slate-50 overflow-y-auto",
        ),
        class_name="flex h-screen font-['Montserrat']",
    )