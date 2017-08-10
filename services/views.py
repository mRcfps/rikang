import uuid
from decimal import Decimal
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.conf import settings

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# import push
import pay

from services import types, events
from services.serializers import NewCommentSerializer
from services.models import Order, Consultation, Summary, Comment, Membership
from users.models import Patient, Doctor
from users.permissions import IsPatient, IsDoctor, IsOwnerOrReadOnly


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


class NewOrderView(APIView):

    permission_classes = (IsAuthenticated, IsPatient)

    def post(self, request):
        try:
            patient = request.user.patient
            if request.data['type'] == types.CONSULTATION:
                # create new consultation order
                doctor = get_object_or_404(Doctor, id=request.data['doctor'], active=True)
                consult = Consultation.objects.create(patient=patient,
                                                      doctor=doctor,
                                                      id=uuid.uuid4().hex)
                if hasattr(patient, 'membership'):
                    if patient.membership.expire > datetime.now():
                        discount = settings.MEMBERSHIP_DISCOUNT
                    else:
                        patient.membership.delete()
                        discount = 1
                else:
                    discount = 1
                cost = Decimal(discount) * doctor.consult_price
                order = Order.objects.create(owner=patient,
                                             provider=doctor,
                                             service_object=consult,
                                             cost=cost)
                data = {
                    'order_no': order.order_no,
                    'discount': discount,
                    'cost': order.cost,
                    'status': order.status,
                    'type': types.CONSULTATION,
                    'doctor': doctor.id,
                    'patient': patient.id,
                    'created': order.created,
                }
                return Response(data, status=status.HTTP_201_CREATED)
            elif request.data['type'] == types.MEMBERSHIP:
                # create new membership order
                mem = Membership.objects.create(patient=patient,
                                                id=uuid.uuid4().hex,
                                                name=request.data['name'],
                                                id_card=request.data['id_card'])
                order = Order.objects.create(owner=patient,
                                             service_object=mem,
                                             cost=settings.MEMBERSHIP_PRICE)
                data = {
                    'order_no': order.order_no,
                    'cost': order.cost,
                    'type': types.MEMBERSHIP,
                    'patient': patient.id,
                    'expire': mem.expire,
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': "不存在的服务类型"},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': "所选择的服务类型缺失必要字段"},
                            status=status.HTTP_400_BAD_REQUEST)


class AcceptOrderView(APIView):

    permission_classes = (IsAuthenticated, IsDoctor)

    def post(self, request):
        order = Order.objects.get(order_no=request.data['order_no'])
        consult = Consultation.objects.get(id=request.data['order_no'])

        if order.status != Order.PAID:
            return Response({'error': "错误的订单状态"}, status=status.HTTP_400_BAD_REQUEST)

        if consult.doctor == request.user.doctor:
            # Change order status
            order.status = Order.UNDERWAY
            order.save()
            # Set consultation start time
            consult.start = datetime.now()
            consult.save()

            # push.send_push_to_user(
            #     message="{}医生接受了您的在线咨询。".format(consult.doctor.name),
            #     user_id=consult.patient.user.id
            # )
            return Response({'accepted': True})
        else:
            return Response({'error': "您无权操作此订单"}, status=status.HTTP_403_FORBIDDEN)


class FinishOrderView(APIView):

    permission_classes = (IsAuthenticated, IsPatient)

    def post(self, request):
        order = Order.objects.get(order_no=request.data['order_no'])
        consult = Consultation.objects.get(id=request.data['order_no'])

        if order.status != Order.UNDERWAY:
            return Response({'error': "订单状态错误"}, status=status.HTTP_400_BAD_REQUEST)

        if order.owner != request.user.patient:
            return Response({'error': "您无权操作此订单"}, status=status.HTTP_403_FORBIDDEN)

        # if datetime.now() - consult.start < timedelta(days=1):
        #     return Response({'error': "尚未到结束订单的时间"}, status=status.HTTP_400_BAD_REQUEST)

        # Change order status
        order.status = Order.FINISHED
        order.save()

        # Change income stats
        doctor = order.service_object.doctor
        income = doctor.income
        income.total += order.cost
        income.suspended += order.cost * Decimal(1 - settings.BROKERAGE_RATIO)
        income.save()

        # push.send_push_to_user(
        #     message='对{}医生的咨询已结束，请及时评价。'.format(order.service.doctor.name),
        #     user_id=patient.user.id
        # )

        return Response({'finished': True})


class CommentView(generics.CreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = NewCommentSerializer

    def perform_create(self, serializer):
        doctor = get_object_or_404(Doctor,
                                   id=self.request.data['doctor'],
                                   active=True)
        order = Order.objects.get(order_no=self.request.data['order_no'])
        serializer.save(patient=self.request.user.patient,
                        doctor=doctor,
                        order=order)

        # calculate new rating for this doctor
        new_rating = serializer.validated_data['ratings']
        comment_num = doctor.comments.count()
        doctor.ratings = (doctor.ratings * (comment_num - 1) + new_rating) / comment_num
        doctor.save()


class PayView(APIView):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        response, created = pay.create_charge(
            service_type=request.data['type'],
            cost=request.data['cost'],
            order_no=request.data['order_no'],
            channel=request.data['channel'],
            client_ip=get_client_ip(request)
        )

        if created:
            # add charge_id to the order
            order = Order.objects.get(order_no=response['order_no'])
            order.charge_id = response['id']
            order.save()

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CancelView(APIView):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        order = get_object_or_404(Order, order_no=request.data['order_no'])

        if order.status != Order.UNPAID:
            return Response({'error': "无法取消订单"},
                            status=status.HTTP_400_BAD_REQUEST)

        order.service_object.delete()
        order.delete()

        return Response({'success': True})


class RefundView(APIView):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        order = get_object_or_404(Order, order_no=request.data['order_no'])

        # Check if this order is in wrong status
        if order.status != Order.PAID:
            return Response({'error': "订单状态错误（未处在已支付等待接受预约状态）"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if this order has been unaccepted for over 2 hours
        # if datetime.now() - order.created < timedelta(hours=2):
        #     return Response({'error': "尚未到可退款时间"},
        #                     status=status.HTTP_400_BAD_REQUEST)

        response, success = pay.refund(request.data['charge_id'])

        if success:
            order = Order.objects.get(order_no=request.data['order_no'])
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
            if types.from_service_name[event_obj['subject']] == types.CONSULTATION:
                order.status = Order.PAID
                order.save()
                return Response(status=status.HTTP_200_OK)
            elif types.from_service_name[event_obj['subject']] == types.MEMBERSHIP:
                mem = Membership.objects.get(id=event_obj['order_no'])
                mem.expire = datetime.now() + timedelta(days=365)
                mem.save()
                return Response(status=status.HTTP_200_OK)
            else:
                # nonexistent charge subject
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.data['type'] == events.REFUND_SUCCEEDED:
            order = Order.objects.get(order_no=event_obj['order_no'])
            order.status = Order.REFUND
            order.save()
            return Response(status=status.HTTP_200_OK)

        elif request.data['type'].startswith('summary'):
            summary_from = datetime.fromtimestamp(event_obj['summary_from'])
            summary_to = datetime.fromtimestamp(event_obj['summary_to'])
            Summary.objects.create(
                summary_type=request.data['type'],
                charges_amount=event_obj['charges_amount'],
                charges_count=event_obj['charges_count'],
                summary_from=summary_from.replace(second=0),
                summary_to=summary_to.replace(second=0)
            )
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestIPView(APIView):

    def get(self, request):
        return Response({'ip': get_client_ip(request)})
