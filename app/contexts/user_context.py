from datetime import datetime, timezone

from flask_dance.contrib.google import google

from app.services.user_service import UserService


def inject_photo_url():
    if not google.authorized:
        return dict()

    exp = google.token['expires_at']
    now = datetime.now(timezone.utc).timestamp()
    if now >= exp:
        return dict()

    user = UserService.me_info()
    photo_url = user['photo_url']
    return dict(photo_url=photo_url)
