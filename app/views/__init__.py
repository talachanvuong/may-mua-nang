from .google_view import google_bp
from .landing_view import landing_dp


def init_app(app):
    app.register_blueprint(google_bp, url_prefix='/login')
    app.register_blueprint(landing_dp, url_prefix='/')
