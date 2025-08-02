from rest_framework_mongoengine.serializers import DocumentSerializer
from taskhub.core.models.enterprise import Enterprise  

class EnterpriseSerializer(DocumentSerializer):
    class Meta:
        model = Enterprise
        fields = '__all__'
