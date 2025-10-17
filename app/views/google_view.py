from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint

from app.services.user_service import UserService

google_bp = make_google_blueprint(
    scope=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ],
    redirect_to='landing.index'
)


@oauth_authorized.connect_via(google_bp)
def logged_in(blueprint, token):
    if not token:
        return False

    resp = blueprint.session.get('/oauth2/v2/userinfo')
    if not resp.ok:
        return False

    rawData = resp.json()
    email = rawData['email']

    data = {
        'display_name': rawData['name'],
        'email': email,
        'photo_url': rawData['picture']
    }

    user = UserService.get_by_email(email)
    if not user:
        user = UserService.create(data)
    else:
        user = UserService.update(user, data)
