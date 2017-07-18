from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, String, Text, Boolean, Integer, Date

connections.create_connection()


class ESQuestion(DocType):

    title = String(required=True)
    department = String()
    body = Text()
    solved = Boolean()
    stars = Integer()
    answer_num = Integer()
    created = Date()

    class Meta:
        doc_type = 'questions'


def search(keyword):
    s = Search(index='rikang_qa')
    s = s.query('match', title=keyword)
    return s.execute()
