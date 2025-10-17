from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, redirect, request, url_for
from flask_dance.contrib.google import google

import app.views as bp
from app.extensions import db


def create_app():
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    bp.init_app(app)

    @app.before_request
    def check_token():
        exclude_routes = ['landing.index', 'google.login', 'google.authorized']
        if request.endpoint in exclude_routes:
            return

        if not google.authorized:
            return redirect(url_for('landing.index'))

        exp = google.token['expires_at']
        now = datetime.now(timezone.utc).timestamp()
        if now >= exp:
            return redirect(url_for('landing.index'))

    return app
