from datetime import datetime, timezone

from app.extensions import db


class Favorite(db.Document):
    place = db.LongField(required=True)
    name = db.StringField(required=True)
    admin1 = db.StringField()
    country = db.StringField()
    latitude = db.FloatField(required=True)
    longitude = db.FloatField(required=True)
    created_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))
    user = db.ObjectIdField(required=True)
