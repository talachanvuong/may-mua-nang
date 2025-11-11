from datetime import datetime, timezone

from flask import request, session
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint
from user_agents import parse

from app.services.track_service import TrackService
from app.services.user_service import UserService
from app.utils.decorators import anonymous_required

google_bp = make_google_blueprint(
    scope=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ],
    redirect_to='weather.search'
)


@google_bp.before_request
@anonymous_required
def _():
    pass


@oauth_authorized.connect_via(google_bp)
def logged_in(blueprint, token):
    raw_data = blueprint.session.get('/oauth2/v2/userinfo').json()
    email = raw_data['email']

    data = {
        'display_name': raw_data['name'],
        'email': email,
        'photo_url': raw_data['picture']
    }

    user = UserService.get_by_email(email)

    if not user:
        user = UserService.create(data)
    else:
        UserService.update(user, data)

    session['user'] = {
        'id': user.id,
        'display_name': user.display_name,
        'email': user.email,
        'photo_url': user.photo_url,
    }

    session.setdefault('theme', 'light')

    raw_ua = request.headers['User-Agent']
    ua = parse(raw_ua)

    track_data = {
        'access_token': token['access_token'],
        'expires_at': datetime.fromtimestamp(token['expires_at'], tz=timezone.utc),
        'os': ua.os.family,
        'browser': ua.browser.family,
        'user': user.id
    }

    TrackService.add(track_data)
