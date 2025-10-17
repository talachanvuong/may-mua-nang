from app.extensions import db


class User(db.Document):
    display_name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    photo_url = db.URLField(required=True)

    meta = {
        'collection': 'users'
    }
