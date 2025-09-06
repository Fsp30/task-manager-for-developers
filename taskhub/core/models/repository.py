import datetime
from datetime import UTC
from mongoengine import Document, StringField, DateTimeField, ReferenceField

class Repository(Document):
    repository_id = StringField(required=True, unique=True)
    admin_repository = ReferenceField('RepositoryPermission')
    creator_Id = ReferenceField('User', required=True)
    enterpriseId = ReferenceField('Enterprise')
    created_at = DateTimeField(default=lambda: datetime.datetime.now(UTC))
    updated_at = DateTimeField(default=lambda: datetime.datetime.now(UTC))
    content_Id = ReferenceField('ContentRepository')

    meta = {
        'collection': 'repositories',
        'indexes': [
            'repository_id',
            'creator_Id',
            'enterpriseId'
        ]
    }

    def save(self, *args, **kwargs) -> None:
        self.updated_at = datetime.datetime.now(UTC)
        super().save(*args, **kwargs)
