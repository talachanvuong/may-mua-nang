from .landing_view import landing_dp


def init_app(app):
    app.register_blueprint(landing_dp, url_prefix='/')
