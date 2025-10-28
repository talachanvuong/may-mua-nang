from .favorite_view import favorite_bp
from .google_view import google_bp
from .landing_view import landing_dp
from .user_view import user_bp
from .weather_view import weather_bp


def init_app(app):
    app.register_blueprint(favorite_bp, url_prefix='/favorite')
    app.register_blueprint(google_bp, url_prefix='/login')
    app.register_blueprint(landing_dp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(weather_bp, url_prefix='/weather')
