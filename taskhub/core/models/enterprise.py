import datetime
from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField

class Enterprise(Document):
    Owner_Id = ReferenceField('User', required=True)
    gitId_enterprise = StringField(max_length=100)
    enterpriseId = StringField(max_length=100, required=True)
    nameEnterprise = StringField(max_length=100)
    repositorys_Id = ListField(ReferenceField('Repository')) 
    created_at = DateTimeField(default=datetime.datetime.utcnow)
