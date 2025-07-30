from rest_framework_mongoengine.serializers import DocumentSerializer
from taskhub.core.models.repositoryPermission import RepositoryPermission

class RepositoryPermissionSerializer(DocumentSerializer):
    class Meta:
        model = RepositoryPermission
        fields = '__all__'
