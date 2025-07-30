from rest_framework_mongoengine.viewsets import ModelViewSet
from taskhub.core.models.user import User 
from taskhub.interfaces.api.serializers.user_serializer import UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
