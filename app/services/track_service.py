from app.models.track import Track


class TrackService:
    @staticmethod
    def add(data):
        track = Track(**data)
        track.save()

    @staticmethod
    def remove(user_id, access_token):
        Track.objects(user=user_id, access_token=access_token).first().delete()

    @staticmethod
    def get_all(user_id):
        return Track.objects(user=user_id)

    @staticmethod
    def get_by_access_token(user_id, access_token):
        return Track.objects(user=user_id, access_token=access_token).first()
