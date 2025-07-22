from django.apps import AppConfig
from taskhub.database.connect import mongo_connect

class ReposConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'repos'

    def ready(self):
        mongo_connect()
