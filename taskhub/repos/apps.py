from django.apps import AppConfig
from ..taskhub.database.connect import connect

class ReposConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'repos'

