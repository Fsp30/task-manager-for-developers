from mongoengine import Document, DictField,ReferenceField,ListField, StringField, DateTimeField
import datetime
from datetime import UTC

class RepositoryPermission(Document):
    repositoryPermissionId = StringField(required=True, unique=True)
    admin_repository = ReferenceField('Repository', required=True)
    admin_users = ListField(ReferenceField('User'))
    created_at = DateTimeField(default=lambda: datetime.datetime.now(datetime.UTC))
    updated_at = DateTimeField(default=lambda: datetime.datetime.now(datetime.UTC))   
    
    meta = {
        'collection': 'repository_permissions',
        'indexes': [
            'admin_repository',
            {'fields': ['admin_repository', 'admin_users'], 'unique': True}
        ]
    }

    def save(self, *args, **kwargs) -> None:
       
        self.updated_at = datetime.datetime.now(datetime.UTC)
        super().save(*args, **kwargs)