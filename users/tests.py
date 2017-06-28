from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from users.models import Doctor, Patient, Information
from home.models import Hospital


class UserTests(APITestCase):
    """Test suite for the user model."""

    def setUp(self):
        """Initialize a user to play with."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test')

    def test_register(self):
        """Ensure we can register an account."""
        url = reverse('users:register')
        data = {'username': 'test2', 'password': 'test2'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
        data = {'username': 'test', 'password': 'newpassword'}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then let's login with the new password
        url = reverse('users:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DoctorTests(APITestCase):
    """Test suite for the doctor model."""

    def setUp(self):
        """Initialize a doctor to play with."""
        self.user = User.objects.create_user(username='doctor', password='doctor')
        self.hospital = Hospital.objects.create(
            name='test',
            location='test',
            rank='3A',
            phone=123456,
            description='test'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Initialize the doctor using API
        url = reverse('users:doctor-init')
        data = {
            'name': 'Dr Test',
            'department': 'NEO',
            'years': 20,
            'title': 'C',
            'hospital': self.hospital.id
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
        new_data = response.data
        new_data['department'] = 'PNE'
        self.client.put(url, new_data, format='json')

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
            'doctor': 1,
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
        self.client = APIClient()

        # include appropriate credentials on all requests
        response = self.client.post(
            reverse('users:login'),
            {'username': 'patient', 'password': 'patient'},
            format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_get_and_update_patient_profile(self):
        """Ensure we can get and update patient's profile."""
        url = reverse('users:patient-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update profile
        data = {
            'user': 1,
            'name': 'test',
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
