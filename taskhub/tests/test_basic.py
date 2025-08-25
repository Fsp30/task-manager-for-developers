import pytest
from django.conf import settings

def test_basic_math():
    assert 1 + 1 == 2

def test_django_available():
    assert settings is not None
    print(f"Settings module: {settings.SETTINGS_MODULE}")
    print(f"DEBUG mode: {settings.DEBUG}")

def test_mongoengine_available():
    try:
        from mongoengine import connect
        assert connect is not None
    except ImportError:
        pytest.fail("MongoEngine não está disponível")

def test_django_settings_configured():

    assert hasattr(settings, 'SECRET_KEY')
    assert hasattr(settings, 'INSTALLED_APPS')
    assert hasattr(settings, 'DATABASES')
    print("Configurações básicas do Django estão presentes")