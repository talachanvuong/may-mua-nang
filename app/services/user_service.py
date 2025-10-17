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
