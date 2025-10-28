from datetime import datetime, timezone
from functools import wraps

from flask import redirect, session, url_for
from flask_dance.contrib.google import google


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not google.authorized:
            return redirect(url_for('landing.index'))

        exp = google.token['expires_at']
        now = datetime.now(timezone.utc).timestamp()

        if now >= exp:
            session.pop('google_oauth_token', None)
            session.pop('user', None)
            session.pop('location', None)

            return redirect(url_for('landing.index'))

        return f(*args, **kwargs)
    return wrapper


def anonymous_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if google.authorized:
            exp = google.token['expires_at']
            now = datetime.now(timezone.utc).timestamp()

            if now < exp:
                return redirect(url_for('user.me'))

        return f(*args, **kwargs)
    return wrapper
