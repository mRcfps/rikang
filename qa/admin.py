from django.contrib import admin

from .models import Question, Answer, AnswerComment


class QuestionAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'department', 'owner',
                    'solved', 'stars', 'updated', 'created')
    list_filter = ('department', 'solved', 'stars', 'created')
    search_fields = ('title', 'department')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(AnswerComment)
