import uuid
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import push

from services import pay, types, events
from services.models import Order, Consultation, Summary
from users.models import Patient, Doctor
from users.permissions import IsPatient, IsDoctor, RikangKeyPermission, IsOwnerOrReadOnly


class NewOrderView(APIView):

    permission_classes = (IsAuthenticated, RikangKeyPermission, IsPatient)

    def post(self, request):
        try:
            if request.data['type'] == types.CONSULTATION:
                patient = Patient.objects.get(id=request.user.patient.id)
                doctor = get_object_or_404(Doctor, id=request.data['doctor'], active=True)
                consult = Consultation.objects.create(patient=patient,
                                                      doctor=doctor,
                                                      id=uuid.uuid4().hex)
                order = Order.objects.create(owner=request.user.patient,
                                             service_object=consult,
                                             cost=doctor.consult_price)

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


class AcceptOrderView(APIView):

    permission_classes = (IsAuthenticated, RikangKeyPermission, IsDoctor)

    def post(self, request):
        order = Order.objects.get(id=request.data['order_no'])
        consult = Consultation.objects.get(id=request.data['order_no'])

        if consult.doctor == request.user.doctor:
            # Change order status
            order.status = Order.UNDERWAY
            order.save()
            # Set consultation start time
            consult.start = datetime.now()
            consult.save()

            push.send_push_to_user(
                message="{}医生接受了您的在线咨询。".format(consult.doctor.name),
                user_id=consult.patient.user.id
            )
            return Response({'accepted': True})
        else:
            return Response({'error': "您无权操作此订单"}, status=status.HTTP_403_FORBIDDEN)


class FinishOrderView(APIView):

    permission_classes = (IsAuthenticated, RikangKeyPermission, IsPatient)

    def post(self, request):
        order = Order.objects.get(id=request.data['order_no'])
        consult = Consultation.objects.get(id=request.data['order_no'])

        if order.owner != request.user.patient:
            return Response({'error': "您无权操作此订单"}, status=status.HTTP_403_FORBIDDEN)

        if datetime.now() - consult.start < timedelta(days=1):
            return Response({'error': "尚未到结束订单的时间"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = Order.FINISHED
        order.save()

        doctor = order.service.doctor
        doctor.order_num += 1
        doctor.save()

        patient = order.service.patient
        push.send_push_to_user(
            message='对{}医生的咨询已结束，请及时评价。'.format(order.service.doctor.name),
            user_id=patient.user.id
        )

        return Response({'finished': True})


class PayView(APIView):

    permission_classes = (IsAuthenticated, RikangKeyPermission, IsOwnerOrReadOnly)

    def post(self, request):
        response, created = pay.create_charge(
            service_type=request.data['type'],
            cost=request.data['cost'],
            order_no=request.data['order_no'],
            channel=request.data['channel'],
            client_ip=request.data['client_ip']
        )

        if created:
            consult = Consultation.objects.get(id=request.data['order_no'])
            push.send_push_to_user(
                message="您有了新的在线咨询订单，请及时查看。",
                user_id=consult.doctor.user.id
            )
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CancelView(APIView):

    permission_classes = (IsAuthenticated, RikangKeyPermission, IsOwnerOrReadOnly)

    def post(self, request):
        order = get_object_or_404(Order, order_no=request.data['order_no'])

        if order.status != Order.UNPAID:
            return Response({'error': "无法取消订单"},
                            status=status.HTTP_400_BAD_REQUEST)

        order.service_object.delete()
        order.delete()

        return Response({'success': True})


class RefundView(APIView):

    permission_classes = (IsAuthenticated, RikangKeyPermission, IsOwnerOrReadOnly)

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

            doctor = order.service.doctor
            patient = order.service.patient
            push.send_push_to_user(
                message="{}医生超过2小时未回复您的咨询请求，咨询费用已全部退还。".format(doctor.name),
                user_id=patient.user.id
            )
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
        elif request.data['type'].startswith('summary'):
            Summary.objects.create(
                summary_type=request.data['type'],
                charges_amount=event_obj['charges_amount'],
                charges_count=event_obj['charges_count'],
                summary_from=datetime.fromtimestamp(event_obj['summary_from']),
                summary_to=datetime.fromtimestamp(event_obj['summary_to'])
            )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
