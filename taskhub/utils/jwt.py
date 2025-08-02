import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_custom_jwt(user):
        payload = {
                'gitId': user.gitId,
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(hours=1),
                'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')    

        return token
