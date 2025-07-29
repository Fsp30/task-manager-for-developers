from rest_framework_mongoengine.serializers import DocumentSerializer
from taskhub.core.models.contentRepository import Task  

class TaskSerializer(DocumentSerializer):
    class Meta:
        model = Task
        fields = '__all__'
