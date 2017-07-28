from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from users.models import Phone, Doctor, Patient, Information
from home.models import Hospital

# Enter your phone number here to test sms verification
TEST_PHONE_NUMBER = '18321025181'


class UserTests(APITestCase):
    """Test suite for the user model."""

    def setUp(self):
        """Initialize a user to play with."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test')

    def test_request_sms_code(self):
        """Ensure we can get sms code."""
        url = reverse('users:request-sms-code')
        data = {'phone': TEST_PHONE_NUMBER}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register(self):
        """Ensure we can register an account with a verified phone number."""
        # Initialize a verified phone instance
        phone = Phone.objects.create(number=TEST_PHONE_NUMBER, verified=True)

        url = reverse('users:register')
        data = {'username': TEST_PHONE_NUMBER, 'password': 'test'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_block_unverified_register_requests(self):
        """Ensure requests with phone numbers not verified can't register an account."""
        url = reverse('users:register')
        data = {'username': 'unverified phone', 'password': 'test'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login(self):
        """Ensure we can login and get a token."""
        url = reverse('users:login')
        data = {'username': 'test', 'password': 'test'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['token'], None)

    def test_block_unregistered_user(self):
        """Ensure an unregistered user cannot login."""
        url = reverse('users:login')
        data = {'username': 'bad guy', 'password': 'reallybad'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_wrong_password(self):
        """Ensure we cannot login when password is wrong."""
        url = reverse('users:login')
        data = {'username': 'test', 'password': 'wrong'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        """Ensure we can change password."""
        url = reverse('users:change-password')
        data = {'old_password': 'test', 'new_password': 'newpassword'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then let's login with the new password
        url = reverse('users:login')
        data = {'username': 'test', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DoctorTests(APITestCase):
    """Test suite for the doctor model."""

    def setUp(self):
        """Initialize a doctor to play with."""
        self.user = User.objects.create_user(username='doctor', password='doctor')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Initialize the doctor using API
        url = reverse('users:doctor-init')
        data = {
            'name': 'Dr Test',
            'department': 'NEO',
            'hospital': 'test',
            'start': '2000-01-01',
            'title': 'C',
        }
        self.client.post(url, data, format='json')
        self.doctor = Doctor.objects.first()

    def test_get_and_update_doctor_profile(self):
        """Ensure we can get and update profile of the doctor."""
        url = reverse('users:doctor-profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.doctor.name)

        # update profile
        new_data = {
            'name': 'Dr Test',
            'department': 'PNE',
            'start': '2000-01-01',
            'title': 'C',
            'hospital': 'test',
        }
        response = self.client.put(url, new_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['department'], new_data['department'])

    def test_get_info(self):
        """Ensure we can get doctor's info."""
        url = reverse('users:doctor-info')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_info(self):
        """Ensure we can update doctor's info."""
        url = reverse('users:doctor-info')
        data = {
            'specialty': 'test',
            'background': 'test',
            'achievements': 'test',
            'motto': 'test',
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['specialty'], data['specialty'])


class PatientTests(APITestCase):
    """Test suite for the patient model."""

    def setUp(self):
        """Initialize a patient to play with."""
        self.user = User.objects.create_user(username='patient', password='patient')
        self.patient = Patient.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_and_update_patient_profile(self):
        """Ensure we can get and update patient's profile."""
        url = reverse('users:patient-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update profile
        data = {'name': 'new_name'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
