from datetime import datetime, timedelta

from flask import session
from flask_dance.contrib.google import google

from app.services.track_service import TrackService


def inject_photo_url():
    if not google.authorized:
        return dict()

    user = session['user']
    track = TrackService.get_by_access_token(user['id'], google.token['access_token'])
    now = datetime.now()

    if not track or now >= track.expires_at + timedelta(hours=7):
        return dict()

    photo_url = user['photo_url']

    return dict(photo_url=photo_url)


def inject_theme():
    if 'theme' not in session:
        return dict()

    return dict(theme=session['theme'])
