from datetime import datetime, timezone

from app.extensions import db


class Log(db.Document):
    message = db.StringField(required=True)
    created_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))
    user = db.ObjectIdField(required=True)
