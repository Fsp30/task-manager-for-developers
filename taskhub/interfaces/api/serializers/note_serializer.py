from rest_framework_mongoengine.serializers import DocumentSerializer
from taskhub.core.models.contentRepository import Note  

class NoteSerializer(DocumentSerializer):
    class Meta:
        model = Note
        fields = '__all__'
