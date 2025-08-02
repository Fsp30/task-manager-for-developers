from rest_framework_mongoengine.serializers import DocumentSerializer
from taskhub.core.models.repository import Repository

class RepositorySerializer(DocumentSerializer):
    class Meta:
        model = Repository
        fields = '__all__'
