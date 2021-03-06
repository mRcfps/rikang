import uuid
from datetime import timedelta, datetime

from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from services.models import Order, Consultation, Comment, Summary, Membership
from users.models import Doctor, Patient

# Number of doctor-comments for test
# Should be larger than PAGE_SIZE
TEST_COMMENT_NUM = 50


class ConsultationOrderTests(APITestCase):
    """Test suite for the whole life cycle of a consultation order."""

    def setUp(self):
        # initialize a doctor
        self.doctor_user = User.objects.create_user(username='doctor', password='test')
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            name='test',
            department='AND',
            hospital='test',
            start='2000-01-01',
            consult_price=50.00,
            title='A',
            active=True
        )

        # initialize a patient
        self.patient_user = User.objects.create_user(username='patient', password='test')
        self.patient = Patient.objects.create(user=self.patient_user)

        # intialize APIClient
        self.client = APIClient()
        self.client.force_authenticate(user=self.patient_user)

        # initialize a consult order
        self.consult = Consultation.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start=datetime.now(),
            id=uuid.uuid4().hex
        )
        self.order = Order.objects.create(owner=self.patient,
                                          provider=self.doctor,
                                          service_object=self.consult,
                                          cost=self.doctor.consult_price)

    def test_create_new_order(self):
        """Ensure we can create a new consult order."""
        url = reverse('services:new-order')
        data = {'type': 'C', 'doctor': self.doctor.id}
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Consultation.objects.count(), 2)

    def test_block_order_with_nonexistent_service_type(self):
        """Ensure we can block orders with unknown types."""
        url = reverse('services:new-order')
        bad_data = {'type': 'A', 'doctor': self.doctor.id}
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, bad_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_block_incomplete_order(self):
        """Ensure we can block orders with some fields missing."""
        url = reverse('services:new-order')
        bad_data = {'type': 'C'}
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, bad_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pay_order(self):
        """Ensure we can go through pay->confirm->refund cycle."""
        url = reverse('services:pay')
        data = {
            'order_no': self.order.order_no,
            'type': 'C',
            'cost': self.order.cost,
            'channel': 'alipay',
            'client_ip': '192.168.0.238',
        }
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if order's status is not changed and has its charge_id
        test_order = Order.objects.get(order_no=self.order.order_no)
        self.assertEqual(test_order.status, Order.UNPAID)
        self.assertEqual(hasattr(test_order, 'charge_id'), True)

        # Post charge-succeeded event to webhooks
        url = reverse('services:webhooks')
        data = {
            "id": "evt_ugB6x3K43D16wXCcqbplWAJo",
            "created": 1427555101,
            "type": "charge.succeeded",
            "data": {
                "object": {
                    "id": "ch_Xsr7u35O3m1Gw4ed2ODmi4Lw",
                    "object": "charge",
                    "created": 1427555076,
                    "app": "app_1Gqj58ynP0mHeX1q",
                    "channel": "upacp",
                    "order_no": self.order.order_no,
                    "client_ip": "127.0.0.1",
                    "amount": 100,
                    "amount_settle": 100,
                    "currency": "cny",
                    "subject": "在线咨询",
                    "body": "Your Body",
                }
            },
        }
        self.client.force_authenticate()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if order's status is switched to PAID
        test_order = Order.objects.get(order_no=self.order.order_no)
        self.assertEqual(test_order.status, Order.PAID)

    def test_accept_order(self):
        """Ensure a doctor can accept a paid order."""
        self.order.status = Order.PAID
        self.order.save()
        url = reverse('services:accept-order')
        data = {'order_no': self.order.order_no}
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if the test order's status has switched to UNDERWAY
        test_order = Order.objects.get(order_no=self.order.order_no)
        self.assertEqual(test_order.status, Order.UNDERWAY)

    def test_cancel_order(self):
        """Ensure we can cancel an order."""
        url = reverse('services:cancel')
        data = {'order_no': self.order.order_no}
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the order and consultation object has been destroyed
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Consultation.objects.count(), 0)

    def test_block_cancel_order_requests_with_wrong_status(self):
        """Ensure orders not in UNPAID status won't be cancelled."""
        self.order.status = Order.FINISHED
        self.order.save()
        url = reverse('services:cancel')
        data = {'order_no': self.order.order_no}
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_finish_order(self):
        """Ensure we can finish an order."""
        self.order.status = Order.UNDERWAY
        self.order.save()

        # rewind a day back to pass time check
        self.consult.start -= timedelta(days=1)
        self.consult.save()

        url = reverse('services:finish-order')
        data = {'order_no': self.order.order_no}
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the order's status is FINISHED
        test_order = Order.objects.get(order_no=self.order.order_no)
        test_consult = Consultation.objects.get(id=self.consult.id)
        self.assertEqual(test_order.status, Order.FINISHED)

    def test_add_new_comment(self):
        """Ensure we can add a new comment to an order."""
        url = reverse('services:comment')
        data = {
            'ratings': 5,
            'doctor': self.doctor.id,
            'body': 'test',
            'order_no': self.order.order_no,
        }
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(Comment.objects.count(), 0)

    def test_patient_get_services(self):
        """Ensure a patient can get all his/her consult orders."""
        url = reverse('users:patient-services')
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class MembershipOrderTests(APITestCase):
    """Test suite for the whole life cycle of a membership order."""

    def setUp(self):
        # initialize a doctor
        self.doctor_user = User.objects.create_user(username='doctor', password='test')
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            name='test',
            department='AND',
            hospital='test',
            start='2000-01-01',
            consult_price=50.00,
            title='A',
            active=True
        )

        # initialize a patient
        self.patient_user = User.objects.create_user(username='patient', password='test')
        self.patient = Patient.objects.create(user=self.patient_user)



        # intialize APIClient
        self.client = APIClient()

        self.mem = Membership.objects.create(patient=self.patient,
                                             id=uuid.uuid4().hex)
        self.order = Order.objects.create(owner=self.patient,
                                          service_object=self.mem,
                                          cost=settings.MEMBERSHIP_PRICE)

    def test_create_new_order(self):
        """Ensure we can create new mem order via api."""
        new_pu = User.objects.create_user(username='new', password='test')
        p = Patient.objects.create(user=new_pu)
        url = reverse('services:new-order')
        data = {'type': 'M', 'name': 'test', 'id_card': 'test'}
        self.client.force_authenticate(user=new_pu)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Membership.objects.count(), 2)
        self.assertEqual(Order.objects.count(), 2)

    def test_cancel_order(self):
        """Ensure we can cancel a mem order."""
        url = reverse('services:cancel')
        data = {'order_no': self.order.order_no}
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Membership.objects.count(), 0)
        self.assertEqual(Order.objects.count(), 0)

    def test_pay_order(self):
        """Ensure we can pay a mem order."""
        url = reverse('services:pay')
        data = {
            'order_no': self.order.order_no,
            'type': 'M',
            'cost': self.order.cost,
            'channel': 'alipay',
        }
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the order's status has not changed and has its charge_id
        test_order = Order.objects.get(order_no=self.order.order_no)
        self.assertEqual(test_order.status, Order.UNPAID)
        self.assertEqual(hasattr(test_order, 'charge_id'), True)

    def test_webhooks_confirm_pay(self):
        """Ensure a webhooks event can activate a membership order."""

        # check if the unpaid membership has no expire time
        self.assertEqual(hasattr(self.mem.refresh_from_db(), 'expire'), False)

        url = reverse('services:webhooks')
        data = {
            "id": "evt_ugB6x3K43D16wXCcqbplWAJo",
            "created": 1427555101,
            "type": "charge.succeeded",
            "data": {
                "object": {
                    "id": "ch_Xsr7u35O3m1Gw4ed2ODmi4Lw",
                    "object": "charge",
                    "created": 1427555076,
                    "app": "app_1Gqj58ynP0mHeX1q",
                    "channel": "upacp",
                    "order_no": self.order.order_no,
                    "client_ip": "127.0.0.1",
                    "amount": 100,
                    "amount_settle": 100,
                    "currency": "cny",
                    "subject": "会员",
                    "body": "Your Body",
                }
            },
        }
        self.client.force_authenticate()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if the membership has its valid expire time
        test_mem = Membership.objects.get(id=self.order.order_no)
        self.assertEqual(hasattr(test_mem, 'expire'), True)

        # check if the user can see the membership
        url = reverse('users:patient-membership')
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['expire'], None)

        # check if this member can create order with discount
        url = reverse('services:new-order')
        data = {
            'type': 'C',
            'doctor': self.doctor.id,
        }
        test_patient = Patient.objects.get(user=self.patient_user)
        self.assertEqual(hasattr(test_patient, 'membership'), True)
        self.assertNotEqual(test_patient.membership.expire, None)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data['discount'], 1)

    def test_non_vip_has_no_valid_membership(self):
        """Ensure a non-vip user cannot see membership."""
        new_user = User.objects.create_user(username='test2', password='test')
        new_patient = Patient.objects.create(user=new_user)
        url = reverse('users:patient-membership')
        self.client.force_authenticate(user=new_user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['expire'], None)


class CommentTests(APITestCase):
    """Test suite for the Comment model."""

    def setUp(self):
        """Initialize a doctor and a patient."""
        doctor_user = User.objects.create_user(username='test_doctor', password='test')
        self.doctor = Doctor.objects.create(
            user=doctor_user,
            name='test_doctor',
            department='GYN',
            hospital='test',
            start='2000-01-01',
            title='A',
            active=True
        )

        patient_user = User.objects.create_user(username='test_patient', password='test')
        self.patient = Patient.objects.create(user=patient_user, name='test_patient')

        # Add comments to the doctor just created
        for _ in range(TEST_COMMENT_NUM):
            Comment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                ratings=5,
                body='test'
            )

        self.client = APIClient()
        self.client.force_authenticate(user=patient_user)

    def test_get_comment_list(self):
        """Ensure we can get all comments of a given doctor."""
        url = reverse('home:doctor-comments', args=[self.doctor.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], TEST_COMMENT_NUM)


class SummaryTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_new_summary(self):
        """Ensure we can create new summaries from pingxx."""
        url = reverse('services:webhooks')
        data = {
            "id": "evt_testtestz79mgOE0MCPN21CM",
            "created": 1440407412,
            "livemode": True,
            "type": "summary.daily.available",
            "data": {
                "object": {
                    "app_id": "app_urj1WLzvzfTK0OuL",
                    "object": "app_daily_summary",
                    "app_display_name": "测试应用",
                    "created": 1440407412,
                    "summary_from": 1440407412,
                    "summary_to": 1440407412,
                    "charges_amount": 3000,
                    "charges_count": 300
                }
            },
            "object": "event",
            "request": "",
            "pending_webhooks": 0
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(Summary.objects.count(), 0)
