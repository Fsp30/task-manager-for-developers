from rest_framework.response import Response

def api_response(success=True, message="", data=None, status_code=200, code=None):
    return Response({
        "success": success,
        "message": message,
        "code": code,
        "status_code": status_code,
        "data": data
    }, status=status_code)
