from rest_framework_mongoengine.viewsets import ModelViewSet
from taskhub.core.models.contentRepository import Note
from taskhub.interfaces.api.serializers.note_serializer import NoteSerializer

class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
