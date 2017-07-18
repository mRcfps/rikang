from django.contrib import admin

from services.models import Order, Consultation, Summary


class OrderAdmin(admin.ModelAdmin):

    list_display = ('order_no', 'service_type', 'owner',
                    'cost', 'status', 'created')
    list_filter = ('status', 'service_type')


class ConsultationAdmin(admin.ModelAdmin):

    list_display = ('doctor', 'patient', 'created')


class SummaryAdmin(admin.ModelAdmin):

    list_display = ('summary_type', 'charges_amount', 'charges_count', 'created')

admin.site.register(Order, OrderAdmin)
admin.site.register(Consultation, ConsultationAdmin)
admin.site.register(Summary, SummaryAdmin)
