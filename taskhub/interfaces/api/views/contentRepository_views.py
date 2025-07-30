from rest_framework_mongoengine.viewsets import ModelViewSet
from taskhub.core.models.contentRepository import ContentRepository
from taskhub.interfaces.api.serializers.contentRepository_serializer import ContentRepositorySerializer

class ContentRepositoryViewSet(ModelViewSet):
    queryset = ContentRepository.objects.all()
    serializer_class = ContentRepositorySerializer
