from datetime import datetime, timedelta

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
        consult = get_object_or_404(Consultation, id=request.data['order_no'])
        consult.delete()

        return Response({'success': True})


class RefundView(APIView):

    def post(self, request):
        consult = get_object_or_404(Consultation, id=request.data['order_no'])

        # Check if this consult is in wrong status
        if consult.status != Consultation.PAID:
            return Response({'error': "订单状态错误（未处在已支付等待接受预约状态）"}
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if this consult has been unaccepted for over 2 hours
        if datetime.now() - consult.created < timedelta(hours=2):
            return Response({'error': "尚未到可退款时间"},
                            status=status.HTTP_400_BAD_REQUEST)

        consult.status = Consultation.FINISHED
        consult.save()
        response = pay.refund(request.data['charge_id'])

        return Response(response)
