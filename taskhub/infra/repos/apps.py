from django.apps import AppConfig
from taskhub.infra.database.mongo.connect_mongo import mongo_connect


class ReposConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taskhub.infra.repos'

    def ready(self):
        mongo_connect()
