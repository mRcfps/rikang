import uuid

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from services.models import Order, Consultation, Comment
from users.models import Doctor, Patient

# Number of doctor-comments for test
# Should be larger than PAGE_SIZE
TEST_COMMENT_NUM = 50


class OrderTests(APITestCase):
    """Test suite for the whole life cycle of Order model."""

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
            id=uuid.uuid4().hex
        )
        self.order = Order.objects.create(owner=self.patient,
                                          provider=self.doctor,
                                          service_object=self.consult,
                                          cost=self.doctor.consult_price)

    def test_create_new_order(self):
        """Ensure we can create a new consult order."""
        url = reverse('services:new-order')
        data = {'type': 'C', 'patient': self.patient.id, 'doctor': self.doctor.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Consultation.objects.count(), 2)

    def test_block_order_with_nonexistent_service_type(self):
        """Ensure we can block orders with unknown types."""
        url = reverse('services:new-order')
        bad_data = {'type': 'A', 'patient': self.patient.id, 'doctor': self.doctor.id}
        response = self.client.post(url, bad_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_block_incomplete_order(self):
        """Ensure we can block orders with some fields missing."""
        url = reverse('services:new-order')
        bad_data = {'type': 'C', 'patient': self.patient.id}
        response = self.client.post(url, bad_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pay_order(self):
        """Ensure we can pay an order."""
        url = reverse('services:pay')
        data = {
            'order_no': self.order.order_no,
            'type': 'C',
            'cost': self.order.cost,
            'channel': 'alipay',
            'client_ip': '192.168.0.238',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancel_order(self):
        """Ensure we can cancel an order."""
        url = reverse('services:cancel')
        data = {'order_no': self.order.order_no}
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
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_new_comment(self):
        """Ensure we can add a new comment to an order."""
        url = reverse('services:comment')
        data = {
            'ratings': 5,
            'doctor': self.doctor.id,
            'body': 'test',
            'order_no': self.order.order_no,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(Comment.objects.count(), 0)


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
