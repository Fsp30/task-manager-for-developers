from mongoengine import Document, DictField,ReferenceField,ListField, StringField

class RepositoryPermission(Document):
    repositoryPermissionId = StringField(required=True, unique=True)
    admin_repository = ReferenceField('Repository', required=True)
    admin_users = ListField(ReferenceField('User'))
    
    meta = {
        'collection': 'repository_permissions',
        'indexes': [
            'admin_repository',
            {'fields': ['admin_repository', 'admin_users'], 'unique': True}
        ]
    }