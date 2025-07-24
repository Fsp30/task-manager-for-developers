from mongoengine import Document, DictField

class RepositoryPermission(Document):
    repositoryPermissionId = DictField()
