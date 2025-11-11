from app.extensions import db


class Track(db.Document):
    access_token = db.StringField(required=True, unique=True)
    expires_at = db.DateTimeField(required=True)
    os = db.StringField(required=True)
    browser = db.StringField(required=True)
    user = db.ObjectIdField(required=True)
