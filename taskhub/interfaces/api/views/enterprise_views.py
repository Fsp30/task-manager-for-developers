from rest_framework_mongoengine.viewsets import ModelViewSet
from taskhub.core.models.enterprise import Enterprise 
from taskhub.interfaces.api.serializers.enterprise_serializer import EnterpriseSerializer

class EnterpriseViewSet(ModelViewSet):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer
