from rest_framework_mongoengine.viewsets import ModelViewSet
from taskhub.core.models.repository import Repository  
from taskhub.interfaces.api.serializers.repository_serializer import RepositorySerializer

class RepositoryViewSet(ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
