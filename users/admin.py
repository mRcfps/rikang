from django.urls import reverse
from django.contrib import admin

from users.models import Phone, Doctor, Patient, Information, Income


class PhoneAdmin(admin.ModelAdmin):

    list_display = ('number', 'verified', 'created')
    list_filter = ('verified', 'created')


def view_info(obj):
    return '<a href="{}">查看详细资料</a>'.format(
        reverse('admin:users_information_change', args=[obj.id])
    )

view_info.allow_tags = True


def verify_doctor(obj):
    if not obj.active:
        return '<a href="{}">进行审核</a>'.format(
            reverse('users:verify-doctor', args=[obj.id])
        )

verify_doctor.allow_tags = True


class DoctorAdmin(admin.ModelAdmin):

    list_display = ('name', 'department', 'hospital', 'title', 'ratings',
                    'patient_num', 'created', view_info, 'active', verify_doctor)
    list_filter = ('department', 'title', 'ratings')
    search_fields = ('name',)

    view_info.short_description = '详细资料'
    verify_doctor.short_description = ''


class PatientAdmin(admin.ModelAdmin):

    list_display = ('phone_number', 'name', 'created')

    def phone_number(self, instance):
        return instance.user.username

    phone_number.short_description = '手机号'


def dispatch_income(obj):
    if obj.suspended != 0:
        return '<a href="{}">支付收入</a>'.format(
            reverse('users:dispatch-income', args=[obj.id])
        )

dispatch_income.allow_tags = True


class IncomeAdmin(admin.ModelAdmin):

    list_display = ('doctor', 'total', 'gained',
                    'suspended', dispatch_income)
    search_fields = ('doctor',)

    dispatch_income.short_description = ''


admin.site.register(Phone, PhoneAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Information)
