from django.contrib import admin

from services.models import Order, Consultation, Summary, Comment, Membership


class OrderAdmin(admin.ModelAdmin):

    list_display = ('order_no', 'service_type', 'owner',
                    'cost', 'status', 'created')
    list_filter = ('status', 'service_type')


class ConsultationAdmin(admin.ModelAdmin):

    list_display = ('doctor', 'patient', 'created')


class MembershipAdmin(admin.ModelAdmin):

    list_display = ('patient', 'name', 'expire', 'id_card')
    list_filter = ('expire',)
    search_fields = ('patient', 'name', 'id_card')


class SummaryAdmin(admin.ModelAdmin):

    list_display = ('summary_type', 'charges_amount', 'charges_count', 'created')


class CommentAdmin(admin.ModelAdmin):

    list_display = ('patient', 'doctor', 'ratings', 'created')

admin.site.register(Order, OrderAdmin)
admin.site.register(Consultation, ConsultationAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(Comment, CommentAdmin)
