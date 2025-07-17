from mongoengine import Document, StringField, DateTimeField, ReferenceField
import datetime

class Task(Document):
        title = StringField(required=True)
        description = StringField()
        created_at = DateTimeField(default=lambda: datetime.datetime.now(datetime.timezone.utc))

        meta = {'collection': 'task'}