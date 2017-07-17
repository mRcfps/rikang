from django.contrib import admin

from users.models import Phone, Doctor, Patient, Information


class PhoneAdmin(admin.ModelAdmin):

    list_display = ('number', 'verified', 'created')
    list_filter = ('verified', 'created')


class DoctorAdmin(admin.ModelAdmin):

    list_display = ('name', 'phone_number', 'department', 'hospital', 'years',
                    'title', 'ratings', 'patient_num', 'created')
    list_filter = ('department', 'hospital', 'title', 'ratings')
    search_fields = ('name',)

    def phone_number(self, instance):
        return instance.user.username

    phone_number.short_description = '手机号'


class PatientAdmin(admin.ModelAdmin):

    list_display = ('phone_number', 'name', 'created')

    def phone_number(self, instance):
        return instance.user.username

    phone_number.short_description = '手机号'


admin.site.register(Phone, PhoneAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
