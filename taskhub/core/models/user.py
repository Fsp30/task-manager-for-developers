import datetime
from mongoengine import Document, StringField, DateTimeField, ListField

class User(Document):
    gitId = StringField(required=True)
    email = StringField(required=True)
    userName = StringField(max_length=100)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    linked_repository_id = ListField(StringField())  
