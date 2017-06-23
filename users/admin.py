from django.contrib import admin

from .models import Doctor, Patient


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hospital', 'category', 'ratings')
    list_filter = ('hospital', 'category', 'ratings')
    search_fields = ('name',)


class PatientAdmin(admin.ModelAdmin):
    '''
        Admin View for Patient
    '''
    list_display = ('id', 'name')

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
