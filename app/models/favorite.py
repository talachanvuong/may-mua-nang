from app.extensions import db


class Favorite(db.Document):
    place = db.LongField(required=True)
    name = db.StringField(required=True)
    admin1 = db.StringField()
    country = db.StringField()
    latitude = db.FloatField(required=True)
    longitude = db.FloatField(required=True)
    user = db.ObjectIdField(required=True)
