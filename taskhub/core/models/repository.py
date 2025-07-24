import datetime
from mongoengine import Document, StringField, DateTimeField, ReferenceField

class Repository(Document):
    repository_id = StringField(required=True)
    admin_repository = ReferenceField('RepositoryPermission') 
    creator_Id = ReferenceField('User', required=True)
    enterpriseId = ReferenceField('Enterprise')
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    content_Id = ReferenceField('ContentRepository')
