from mongoengine import Document, StringField, DateTimeField, BooleanField 
import datetime

class Task(Document):
    title = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    closed = BooleanField(required=True)
