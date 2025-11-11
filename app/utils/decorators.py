from datetime import datetime, timedelta
from functools import wraps

from flask import redirect, session, url_for
from flask_dance.contrib.google import google

from app.services.track_service import TrackService


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not google.authorized:
            return redirect(url_for('landing.index'))

        user = session['user']
        track = TrackService.get_by_access_token(user['id'], google.token['access_token'])
        now = datetime.now()

        if not track or now >= track.expires_at + timedelta(hours=7):
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
            user = session['user']
            track = TrackService.get_by_access_token(user['id'], google.token['access_token'])
            now = datetime.now()

            if track and now < track.expires_at + timedelta(hours=7):
                return redirect(url_for('user.me'))

        return f(*args, **kwargs)
    return wrapper
