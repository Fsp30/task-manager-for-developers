import datetime
from datetime import UTC
from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField

class Enterprise(Document):
    owner_Id = ReferenceField('User', required=True)
    devs_enterprise = ListField(ReferenceField('User'))
    gitId_enterprise = StringField(max_length=100, unique=True)
    enterpriseId = StringField(max_length=100, required=True, unique=True)
    nameEnterprise = StringField(max_length=100, required=True, unique=True)
    repositorys_Id = ListField(ReferenceField('Repository')) 
    created_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))

    meta = {
        'collection': 'enterprises', 
        'indexes': [
            'enterpriseId',
            'nameEnterprise', 
            {'fields': ['created_at'], 'expireAfterSeconds': 3600*24*365},
        ]
    }

    def save(self, *args, **kwargs) -> None:
        self.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)
        super().save(*args, **kwargs)