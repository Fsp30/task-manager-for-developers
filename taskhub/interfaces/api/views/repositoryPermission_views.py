from rest_framework_mongoengine.viewsets import ModelViewSet
from taskhub.core.models.repositoryPermission import RepositoryPermission
from taskhub.interfaces.api.serializers.repositoryPermission_serializer import RepositoryPermissionSerializer

class RepositoryPermissionViewSet(ModelViewSet):
    queryset = RepositoryPermission.objects.all()
    serializer_class = RepositoryPermissionSerializer
