import uuid
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from services import pay, types, events
from services.models import Order, Consultation
from users.models import Patient, Doctor


class NewOrderView(APIView):

    def post(self, request):
        try:
            if request.data['type'] == types.CONSULTATION:
                patient = Patient.objects.get(id=request.user.patient.id)
                doctor = Doctor.objects.get(id=request.data['doctor'])
                consult = Consultation.objects.create(patient=patient,
                                                      doctor=doctor,
                                                      id=uuid.uuid4().hex)
                order = Order.objects.create(service_object=consult, cost=doctor.consult_price)

                data = {
                    'order_no': order.order_no,
                    'cost': order.cost,
                    'status': order.status,
                    'type': types.CONSULTATION,
                    'doctor': doctor.id,
                    'patient': patient.id,
                    'created': order.created,
                }

                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': "不存在的服务类型"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': "所选择的服务类型缺失必要字段"},
                            status=status.HTTP_400_BAD_REQUEST)


class PayView(APIView):

    def post(self, request):
        response, created = pay.create_charge(
            service_type=request.data['type'],
            cost=request.data['cost'],
            order_no=request.data['order_no'],
            channel=request.data['channel'],
            client_ip=request.data['client_ip']
        )

        if created:
            order = get_object_or_404(Order, order_no=request.data['order_no'])
            order.status = Order.PAID
            order.save()
            return Response(response)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CancelView(APIView):

    def post(self, request):
        order = get_object_or_404(Order, order_no=request.data['order_no'])

        if order.status != Order.UNPAID:
            return Response({'error': "无法取消订单"},
                            status=status.HTTP_400_BAD_REQUEST)

        order.service_object.delete()
        order.delete()

        return Response({'success': True})


class RefundView(APIView):

    def post(self, request):
        order = get_object_or_404(Order, order_no=request.data['order_no'])

        # Check if this order is in wrong status
        if order.status != Order.PAID:
            return Response({'error': "订单状态错误（未处在已支付等待接受预约状态）"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if this order has been unaccepted for over 2 hours
        if datetime.now() - order.created < timedelta(hours=2):
            return Response({'error': "尚未到可退款时间"},
                            status=status.HTTP_400_BAD_REQUEST)

        response, success = pay.refund(request.data['charge_id'])

        if success:
            order.status = Order.REFUND
            order.save()
            return Response(response)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class WebhooksView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        event_obj = request.data['data']['object']
        if request.data['type'] == events.CHARGE_SUCCEEDED:
            order = Order.objects.get(order_no=event_obj['order_no'])
            order.status = Order.PAID
            order.save()
            return Response(status=status.HTTP_200_OK)
        elif request.data['type'] == events.REFUND_SUCCEEDED:
            order = Order.objects.get(order_no=event_obj['order_no'])
            order.status = Order.REFUND
            order.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
