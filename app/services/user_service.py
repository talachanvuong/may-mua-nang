from app.models.user import User


class UserService:
    @staticmethod
    def create(data):
        user = User(**data)
        user.save()
        return user

    @staticmethod
    def get_by_email(email):
        return User.objects(email=email).first()

    @staticmethod
    def update(user, data):
        user.update(**data)
        user.reload()
