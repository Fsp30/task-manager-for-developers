from rest_framework_mongoengine.viewsets import ModelViewSet
from taskhub.core.models.contentRepository import Task  
from taskhub.interfaces.api.serializers.task_serializer import TaskSerializer

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
