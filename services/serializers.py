from rest_framework import serializers

from services.models import Order, Consultation, Comment
from users.serializers import PatientSerializer


class ConsultationSerializer(serializers.ModelSerializer):

    patient = PatientSerializer()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Consultation
        fields = ('doctor', 'patient', 'status')

    def get_status(self, consult):
        order = Order.objects.get(order_no=consult.id)
        return order.status


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


class NewCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('anonymous', 'ratings', 'body', 'order')
