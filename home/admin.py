from django.contrib import admin
from django.contrib.auth.models import Group

from rest_framework.authtoken.models import Token

from home.models import Post, Hospital


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'created')
    list_filter = ('created',)
    search_fields = ('title',)


class HospitalAdmin(admin.ModelAdmin):

    list_display = ('name', 'location', 'rank', 'phone')
    list_filter = ('rank',)

admin.site.register(Post, PostAdmin)
admin.site.register(Hospital, HospitalAdmin)

# AdminSite settings
admin.site.site_header = '日康 | 后台管理'
admin.site.site_title = '后台管理'

# Unregister unwanted models
admin.site.unregister(Token)
admin.site.unregister(Group)
