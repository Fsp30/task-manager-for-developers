import datetime
from mongoengine import Document, StringField, DateTimeField, DictField, ReferenceField, ListField, BooleanField

class ContentRepository(Document):
    repositoryId = ReferenceField('Repository')
    contentId = StringField(required=True)
    admin_users = ReferenceField('RepositoryPermission')
    working_tag = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    chat_id = StringField(unique=True)
    content_type = StringField(required=True, default='content_repository')
    meta = {
        'allow_inheritance': True,
        'indexes': ['repositoryId', 'created_at', 'content_type']
    }

class Note(ContentRepository):
    title = StringField(max_length=120, required=True)
    author = ReferenceField('User')
    text = StringField(max_length=5000, required=True)  
    tags = ListField(StringField(max_length=50))
    meta = {
        'indexes': ['author', 'title']
    }

class Task(ContentRepository):
    taskId = StringField(required=True, unique=True)
    title = StringField(required=True, max_length=120)
    author = ReferenceField('User')
    resolversId = ListField(ReferenceField('User'))
    description = StringField(max_length=5000)
    status = StringField(choices=('pending', 'in_progress', 'completed', 'cancelled'), default='pending')
    priority = StringField(choices=('low', 'medium', 'high'), default='medium')
    deadline = DateTimeField()
    tags = ListField(StringField(max_length=50))
    task_tag = DictField()
    meta = {
        'indexes': ['author', 'resolversId', 'status', 'priority', 'deadline']
    }