import elasticsearch_dsl
import elasticsearch_dsl.connections

from django.core.management import BaseCommand

from qa.models import Question
from qa.es_docs import ESQuestion


class Command(BaseCommand):

    help = "Index all data to Elasticsearch"

    def handle(self, *args, **options):
        elasticsearch_dsl.connections.connections.create_connection()
        for question in Question.objects.all():
            esq = ESQuestion(
                meta={'id': question.pk},
                title=question.title,
                department=question.department,
                body=question.body,
                solved=question.solved,
                stars=question.stars,
                answer_num=question.answer_num,
                created=question.created
            )
            esq.save(index='rikang_qa')

            self.stdout.write(self.style.SUCCESS(
                'Successfully index Question No.{} into elasticsearch engine.'.format(question.pk)
            ))
