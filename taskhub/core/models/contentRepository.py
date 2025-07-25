import datetime
from mongoengine import Document, StringField, DateTimeField, DictField, ReferenceField, ListField, BooleanField

class ContentRepository(Document):
    repositoryId = ReferenceField('Repository')
    discussionId = StringField(required=True)
    tag = DictField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    chat_id = StringField()

class Note(ContentRepository):
    title = StringField(max_length=120, required=True)
    author = ReferenceField('User')
    text = StringField(max_length=120, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class Task(ContentRepository):
    title = StringField(required=True)
    author = ReferenceField('User')
    resolversId = ListField(ReferenceField('User'))
    description = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    completed = BooleanField()
    tag = DictField()
