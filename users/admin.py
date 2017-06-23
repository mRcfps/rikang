from django.contrib import admin

from .models import Doctor, Patient


class DoctorAdmin(admin.ModelAdmin):

    list_display = ('department', 'name', 'hospital',
                    'title', 'ratings', 'patient_num', 'created')
    list_filter = ('department', 'hospital', 'title', 'ratings')
    search_fields = ('name',)


class PatientAdmin(admin.ModelAdmin):

    list_display = ('name', 'created')

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
