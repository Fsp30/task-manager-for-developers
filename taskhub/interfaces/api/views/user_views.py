from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from taskhub.interfaces.api.authentication.jwt_auth import JWTMongoAuthentication
from taskhub.interfaces.api.serializers.user_serializer import UserSerializer

class MeView(APIView):
    authentication_classes = [JWTMongoAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
