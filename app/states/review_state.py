import reflex as rx
from app.models import ReviewSettings


class ReviewState(rx.State):
    """Manages review settings for exams."""

    settings: dict[str, ReviewSettings] = {}

    @rx.event
    def on_mount(self):
        pass

    @rx.event
    def get_setting(self, exam_title: str) -> ReviewSettings:
        if exam_title not in self.settings:
            self.settings[exam_title] = ReviewSettings(
                exam_id=0, review_enabled=False, exam_mode="Assessment"
            )
        return self.settings[exam_title]

    @rx.event
    def toggle_review(self, exam_title: str):
        setting = self.get_setting(exam_title)
        setting.review_enabled = not setting.review_enabled
        self.settings[exam_title] = setting

    @rx.event
    def set_mode(self, exam_title: str, mode: str):
        setting = self.get_setting(exam_title)
        setting.exam_mode = mode
        self.settings[exam_title] = setting