from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from taskhub.interfaces.api.constants.status_codes import AppCode
from taskhub.interfaces.api.constants.status_codes import ErrorsAppStatus
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({
            "success": False,
            "message": str(exc.detail) if hasattr(exc, 'detail') else str(exc),
            "status_code": response.status_code,
            "code": getattr(exc, 'app_code', None),
            "data": None
        }, status=response.status_code)
    else:
        logger.exception("Erro interno inesperado")
        return Response({
            "success": False,
            "message": "Erro interno do servidor",
            "status_code": ErrorsAppStatus.SERVER_ERROR,
            "code": None,
            "data": None
        }, status=ErrorsAppStatus.SERVER_ERROR)


class CustomAppException(APIException):
    status_code = ErrorsAppStatus.BAD_REQUEST
    default_detail = "Erro na aplicação"
    default_code = "application_error"
    app_code = None





class ExternalAPIError(CustomAppException):
    status_code = ErrorsAppStatus.SERVICE_UNAVAILABLE
    default_detail = "Erro ao comunicar com serviço externo."
    default_code = "external_api_error"
    app_code = AppCode.AUTH_GITHUB_CALLBACK_ERROR
