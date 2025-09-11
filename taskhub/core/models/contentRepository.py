import datetime
from datetime import UTC
from mongoengine import Document, StringField, DateTimeField, DictField, ReferenceField, ListField, BooleanField

class ContentRepository(Document):
    repositoryId = ReferenceField('Repository')
    contentId = StringField(required=True, unique=True)
    admin_users = ReferenceField('RepositoryPermission')
    working_tag = StringField()
    created_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    chat_id = StringField(unique=True)
    content_type = StringField(required=True, default='content_repository')
    notes = ListField(ReferenceField('Note'))
    tasks = ListField(ReferenceField('Task'))
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
        'indexes': ['author', 'title'],
        'content_type': 'note'
    }

class Task(ContentRepository):
    taskId = StringField(required=True, unique=True)
    link_content_id = ReferenceField('ContentRepository') 
    title = StringField(required=True, max_length=120)
    author = ReferenceField('User')
    resolvers = ListField(ReferenceField('User'))
    description = StringField(max_length=5000)
    status = StringField(choices=('pending', 'in_progress', 'completed', 'cancelled'), default='pending')
    priority = StringField(choices=('low', 'medium', 'high'), default='medium')
    deadline = DateTimeField()
    tags = ListField(StringField(max_length=50))
    created_task_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_task_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    
    meta = {
        'indexes': [
            'author',
            'resolvers',
            'status',
            'priority',
            'deadline',
            'link_content_id'  
        ],
        'content_type': 'task'
    }
    
    def save(self, *args, **kwargs):
        self.updated_task_at = datetime.datetime.now(tz=datetime.timezone.utc)
        super().save(*args, **kwargs)