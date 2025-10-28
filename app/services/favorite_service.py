from app.models.favorite import Favorite


class FavoriteService:
    @staticmethod
    def add(data):
        favorite = Favorite(**data)
        favorite.save()

    @staticmethod
    def remove(user_id, place):
        Favorite.objects(user=user_id, place=place).first().delete()

    @staticmethod
    def get_all(user_id):
        return Favorite.objects(user=user_id)

    @staticmethod
    def get_by_place(user_id, place):
        return Favorite.objects(user=user_id, place=place).first()
