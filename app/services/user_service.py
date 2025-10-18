from flask_dance.contrib.google import google

from app.models.user import User


class UserService:
    @staticmethod
    def create(data):
        user = User(**data)
        user.save()
        return user

    @staticmethod
    def get_by_email(email):
        user = User.objects(email=email).first()
        if not user:
            return None

        return user

    @staticmethod
    def update(user, data):
        user.update(**data)
        return user

    @staticmethod
    def fetch():
        resp = google.get('/oauth2/v2/userinfo')
        data = resp.json()
        return data

    @staticmethod
    def me_info():
        data = UserService.fetch()
        email = data['email']

        user = UserService.get_by_email(email)
        return user
