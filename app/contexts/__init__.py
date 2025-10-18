from .user_context import inject_photo_url


def init_app(app):
    app.context_processor(inject_photo_url)
