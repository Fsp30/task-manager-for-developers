from rest_framework_mongoengine.serializers import DocumentSerializer
from taskhub.core.models.user import User

class UserSerializer(DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'
