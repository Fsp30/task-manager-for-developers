import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from taskhub.core.models.user import User

class JWTMongoAuthentication(BaseAuthentication):
        def authenticate(self, request):
                auth_header = request.headers.get('Authorization')
                
                if not auth_header or not auth_header.startswith('Bearer '):
                        return None
                
                token = auth_header.split(' ')[1]
                try:
                        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
                        user = User.objects(gitId=payload['gitId']).first()
                        if not user:
                                raise AuthenticationFailed('Usuário não encontrado')
                
                except jwt.ExpiredSignatureError:
                        raise AuthenticationFailed('Token expirado')
                except jwt.InvalidTokenError:
                        raise AuthenticationFailed('Token inválido')

                return (user, None)
        
        