from app.models.log import Log


class LogService:
    @staticmethod
    def add(data):
        log = Log(**data)
        log.save()

    @staticmethod
    def get_all(user_id):
        return Log.objects(user=user_id).order_by('-created_at')
