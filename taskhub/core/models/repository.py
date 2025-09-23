import datetime
from datetime import timezone
from mongoengine import Document, StringField, DateTimeField, ReferenceField

class Repository(Document):
    repository_id = StringField(required=True, unique=True)
    creator_Id = ReferenceField('User', required=True)
    enterpriseId = ReferenceField('Enterprise')
    created_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
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
        self.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)
        super().save(*args, **kwargs)
