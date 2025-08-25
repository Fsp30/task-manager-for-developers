import datetime
from datetime import UTC
from typing import TYPE_CHECKING
from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField


class User(Document):
    gitId = StringField(required=True, unique=True, max_length=100)
    email = StringField(required=True, max_length=255, unique=True)  
    userName = StringField(required=True, max_length=100) 
    created_at = DateTimeField(default=lambda: datetime.datetime.now(datetime.UTC))
    updated_at = DateTimeField(default=lambda: datetime.datetime.now(datetime.UTC))   
    repositories = ListField(ReferenceField('Repository'))
    enterprise = ReferenceField('Enterprise')
    repository_permissions = ListField(ReferenceField('RepositoryPermission'))
    tasks = ListField(ReferenceField('Task'))
    
    meta = {
        'collection': 'users',
        'indexes': [
            'gitId',
            'email',
            'userName',
            'enterprise',
            {'fields': ['repositories'], 'sparse': True},
            {'fields': ['tasks'], 'sparse': True}
        ]
    }
    
    @property
    def is_authenticated(self) -> bool:
        return True
    
    def save(self, *args, **kwargs) -> None:
       
        self.updated_at = datetime.datetime.now(datetime.UTC)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"User: {self.userName} ({self.gitId})"