from dotenv import load_dotenv
from flask import Flask

import app.views as bp
from app.extensions import db


def create_app():
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    bp.init_app(app)

    return app
