from datetime import datetime, timedelta

from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_dance.contrib.google import google

from app.services.track_service import TrackService
from app.utils.decorators import token_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/me', methods=['GET', 'POST'])
@token_required
def me():
    if request.method == 'POST':
        theme = request.form['theme']
        session['theme'] = theme

        return redirect(url_for('user.me'))

    user = session['user']
    tracks = TrackService.get_all(user['id'])
    now = datetime.now()

    for track in tracks:
        track.is_this_device = google.token['access_token'] == track['access_token']
        track.is_valid = now < track.expires_at + timedelta(hours=7)

    return render_template('user_me.html', user=user, tracks=tracks)


@user_bp.route('/logout')
@token_required
def logout():
    session.pop('google_oauth_token', None)
    session.pop('user', None)
    session.pop('location', None)

    return redirect(url_for('landing.index'))
