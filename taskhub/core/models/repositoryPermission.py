from mongoengine import Document, DictField,ReferenceField,ListField, StringField, DateTimeField
import datetime
from datetime import UTC

class RepositoryPermission(Document):
    repositoryPermissionId = StringField(required=True, unique=True)
    admin_repository = ReferenceField('Repository', required=True)
    admin_users = ListField(ReferenceField('User'))
    created_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))   
    
    meta = {
        'collection': 'repository_permissions',
        'indexes': [
            'admin_repository',
            {'fields': ['admin_repository', 'admin_users'], 'unique': True}
        ]
    }

    def save(self, *args, **kwargs) -> None:
       
        self.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)
        super().save(*args, **kwargs)