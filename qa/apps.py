from django.apps import AppConfig

from elasticsearch_dsl.connections import connections


class QaConfig(AppConfig):
    name = 'qa'

    def ready(self):
        connections.create_connection()
