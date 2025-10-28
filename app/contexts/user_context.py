from datetime import datetime, timezone

from flask import session
from flask_dance.contrib.google import google


def inject_photo_url():
    if not google.authorized:
        return dict()

    exp = google.token['expires_at']
    now = datetime.now(timezone.utc).timestamp()

    if now >= exp:
        return dict()

    user = session['user']
    photo_url = user['photo_url']

    return dict(photo_url=photo_url)


def inject_theme():
    if 'theme' not in session:
        return dict()

    return dict(theme=session['theme'])
