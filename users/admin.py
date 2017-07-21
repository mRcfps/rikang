from django.urls import reverse
from django.contrib import admin

from users.models import Phone, Doctor, Patient, Information


class PhoneAdmin(admin.ModelAdmin):

    list_display = ('number', 'verified', 'created')
    list_filter = ('verified', 'created')


def view_info(obj):
    if obj.active:
        return '<a href="{}">查看详细资料</a>'.format(
            reverse('admin:users_information_change', args=[obj.id])
        )
    else:
        return None

view_info.allow_tags = True


class DoctorAdmin(admin.ModelAdmin):

    list_display = ('name', 'phone_number', 'department', 'hospital', 'years',
                    'title', 'ratings', 'patient_num', 'created', view_info, 'active')
    list_filter = ('department', 'title', 'ratings')
    list_editable = ('active',)
    search_fields = ('name',)

    def phone_number(self, instance):
        return instance.user.username

    phone_number.short_description = '手机号'
    view_info.short_description = '详细资料'


class PatientAdmin(admin.ModelAdmin):

    list_display = ('phone_number', 'name', 'created')

    def phone_number(self, instance):
        return instance.user.username

    phone_number.short_description = '手机号'


admin.site.register(Phone, PhoneAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Information)
