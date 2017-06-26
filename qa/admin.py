from django.contrib import admin

from .models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'department', 'patient',
                    'solved', 'stars', 'updated', 'created')
    list_filter = ('department', 'solved', 'stars', 'created')
    search_fields = ('title', 'department')

admin.site.register(Question, QuestionAdmin)
