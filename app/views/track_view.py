from flask import Blueprint, redirect, request, session, url_for

from app.services.track_service import TrackService
from app.utils.decorators import token_required

track_bp = Blueprint('track', __name__)


@track_bp.route('/remove', methods=['POST'])
@token_required
def remove():
    user = session['user']

    access_token = request.form['access_token']

    TrackService.remove(user['id'], access_token)

    return redirect(url_for('user.me'))
