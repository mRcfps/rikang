from rest_framework import serializers

from services.models import Order, Consultation


class ConsultationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultation
        fields = ('doctor', 'patient')


class ConsultationOrderSerializer(serializers.ModelSerializer):

    order_no = serializers.SerializerMethodField()
    service_type = serializers.CharField(source='service_type.model')
    service_object = ConsultationSerializer()

    class Meta:
        model = Order
        fields = ('order_no', 'owner', 'cost', 'status', 'created',
                  'service_type', 'service_object')

    def get_order_no(self, order):
        return order.order_no.hex
