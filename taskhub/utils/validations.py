import re
from taskhub.middlewares.exceptions.base_exception_handler import InvalidEmailFormat

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class Validations:
    def validate_email(email: str) -> bool:
        if not EMAIL_REGEX.match(email):
            raise InvalidEmailFormat(f"Invalid email format: {email}")
        return True
