import pytest
from taskhub.middlewares.exceptions import UserAlreadyExists
from taskhub.core.services.user_service import create_user

@pytest.mark.django_db
def test_create_user_duplicate():
    create_user("123", "filipe@example.com", "Filipe")

    with pytest.raises(UserAlreadyExists):
        create_user("123", "filipe@example.com", "Filipe")
