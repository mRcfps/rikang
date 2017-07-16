from django.apps import AppConfig

from elasticsearch_dsl.connections import connections


class QaConfig(AppConfig):
    name = 'qa'
    verbose_name = "问答社区"

    def ready(self):
        connections.create_connection()
