from .location_context import inject_location
from .user_context import inject_photo_url
from .user_context import inject_theme


def init_app(app):
    app.context_processor(inject_location)
    app.context_processor(inject_photo_url)
    app.context_processor(inject_theme)
