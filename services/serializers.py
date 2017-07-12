from rest_framework import serializers

from services.models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(source='doctor.consult_price',
                                     max_digits=10,
                                     decimal_places=2,
                                     required=False)

    class Meta:
        model = Consultation
        fields = ('id', 'doctor', 'patient', 'doctor',
                  'price', 'status', 'created')
