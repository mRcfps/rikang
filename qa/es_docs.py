from elasticsearch_dsl import DocType, String, Text, Boolean, Integer, Date


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
