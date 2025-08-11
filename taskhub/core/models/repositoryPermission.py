from mongoengine import Document, DictField,ReferenceField,ListField

class RepositoryPermission(Document):
    repositoryPermissionId = DictField(requred=True)
    admin_repository = ReferenceField('Repository', required=True)
    admin_users = ListField(ReferenceField('User'))
    
    meta = {
        'collection': 'repository_permissions',
        'indexes': [
            'admin_repository',
            {'fields': ['admin_repository', 'admin_users'], 'unique': True}
        ]
    }