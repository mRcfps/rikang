from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from services import pay
from services.models import Consultation
from services.serializers import ConsultationSerializer


class CreateConsultationView(generics.CreateAPIView):

    serializer_class = ConsultationSerializer


class PayView(APIView):

    def post(self, request):
        response, created = pay.create_charge(
            amount=request.data['amount'],
            order_no=request.data['order_no'],
            channel=request.data['channel'],
            client_ip=request.data['client_ip']
        )

        if created:
            consultation = Consultation.objects.get(id=request.data['order_no'])
            consultation.status = Consultation.PAID
            consultation.save()
            return Response(response)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CancelPayView(APIView):

    def post(self, request):
        consultation = get_object_or_404(Consultation, id=request.data['order_no'])
        consultation.delete()

        return Response({'success': True})
