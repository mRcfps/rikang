from rest_framework import serializers

from services.models import Order, Consultation, Comment
from home.serializers import CommentDisplaySerializer
from users.serializers import PatientSerializer


class ConsultationSerializer(serializers.ModelSerializer):

    patient = PatientSerializer()

    class Meta:
        model = Consultation
        fields = ('doctor', 'patient')


class ConsultationOrderSerializer(serializers.ModelSerializer):

    order_no = serializers.SerializerMethodField()
    service_type = serializers.CharField(source='service_type.model')
    service_object = ConsultationSerializer()
    comment = CommentDisplaySerializer()

    class Meta:
        model = Order
        fields = ('order_no', 'owner', 'cost', 'status', 'created',
                  'service_type', 'service_object', 'comment')

    def get_order_no(self, order):
        return order.order_no.hex


class NewCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('anonymous', 'ratings', 'body', 'order')
