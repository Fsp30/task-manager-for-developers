from rest_framework_mongoengine.serializers import DocumentSerializer
from taskhub.core.models.contentRepository import ContentRepository

class ContentRepositorySerializer(DocumentSerializer):
    class Meta:
        model = ContentRepository
        fields = '__all__'
