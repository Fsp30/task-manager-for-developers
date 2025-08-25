

class BaseTestException(Exception):
    status_code = 400
    default_detail = "Test exception"
    default_code = "test_error"
    app_code = None

    def __init__(self, detail=None):
        if detail:
            self.detail = detail
        else:
            self.detail = self.default_detail
        super().__init__(self.detail)

class CustomAppException(BaseTestException):
    status_code = 400
    default_detail = "Erro na aplicação"
    default_code = "application_error"
    app_code = None

class InputExceededCharacterLimit(BaseTestException):
    status_code = 400
    default_detail = "Valor de input excede o permitido"
    default_code = "length_input_max_invalid"
    app_code = "INPUT_EXCEEDED_CHARACTER_LIMIT"

class InvalidEmailFormat(BaseTestException):
    status_code = 400
    default_detail = "Falha ao adicionar email"
    default_code = "verification_email_no_match"
    app_code = "USER_INVALID_EMAIL"

class ExternalAPIError(BaseTestException):
    status_code = 503
    default_detail = "Erro ao comunicar com serviço externo"
    default_code = "external_api_error"
    app_code = "AUTH_GITHUB_CALLBACK_ERROR"