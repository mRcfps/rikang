from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from home.models import Post, Hospital
from users.models import Doctor, Patient, Information, FavoritePost, FavoriteDoctor

# Number of news for test
# Should be larger than PAGE_SIZE
TEST_POST_NUM = 20

# Number of hospitals for test
# Should be larger than PAGE_SIZE
TEST_HOSPITAL_NUM = 30

# Number of doctors for test
# Should be larger than PAGE_SIZE
TEST_DOCTOR_NUM = 40


class PostTests(APITestCase):
    """Test suite for the post model."""

    def setUp(self):
        """Initialize several posts to play with."""
        self.user = User.objects.create_user(username='test', password='test')
        self.patient = Patient.objects.create(user=self.user)

        for index in range(TEST_POST_NUM):
            content = 'Test {}'.format(index)
            post = Post.objects.create(title=content, body=content)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.test_post = Post.objects.first()

    def test_get_post_list(self):
        """Ensure we can get a list of posts."""
        url = reverse('home:post-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], TEST_POST_NUM)

        # Test if pagination works
        self.assertNotEqual(response.data['next'], None)

    def test_get_post_by_id(self):
        """Ensure we can get one single post by id."""
        url = reverse('home:post-detail', args=[self.test_post.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.test_post.id)

    def test_fav_and_unfav_post(self):
        """Ensure a patient can make a post his/her favorites."""
        url = reverse('home:post-fav', args=[self.test_post.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.patient.favorite_posts.count(), 0)

        # then unfav the post
        url = reverse('home:post-unfav', args=[self.test_post.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.patient.favorite_posts.count(), 0)

    def test_get_all_fav_posts(self):
        """Ensure a patient can get all his/her favorite posts."""
        # supppose this patient has favved all test posts
        for post in Post.objects.all():
            FavoritePost.objects.create(patient=self.patient, post=post)

        url = reverse('users:patient-fav-posts')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], TEST_POST_NUM)


class HospitalTests(APITestCase):
    """Test suite for the hospital model."""

    def setUp(self):
        """Initialize several hospitals to play with."""
        self.user = User.objects.create_user(username='test', password='test')

        for _ in range(TEST_HOSPITAL_NUM):
            Hospital.objects.create(name='test', rank='3A', phone=123456)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.test_hospital = Hospital.objects.first()

    def test_get_hospital_list(self):
        """Ensure we can get a list of hospitals."""
        url = reverse('home:hospital-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], TEST_HOSPITAL_NUM)

        # Test if pagination works
        self.assertNotEqual(response.data['next'], None)

    def test_get_hospital_by_id(self):
        """Ensure we can get one single hospital by id."""
        url = reverse('home:hospital-detail', args=[self.test_hospital.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.test_hospital.id)


class DoctorTests(APITestCase):
    """Test suite for the doctor model in home app."""

    def setUp(self):
        """Initialize several doctors to play with."""
        self.user = User.objects.create_user(username='test', password='test')
        self.patient = Patient.objects.create(user=self.user)

        for index in range(TEST_DOCTOR_NUM):
            user = User.objects.create_user(username=str(index), password='test')
            doctor = Doctor.objects.create(
                user=user,
                name='doctor {}'.format(index),
                department='NEO',
                hospital='test',
                start='2000-01-01',
                title='C',
                active=True
            )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.test_doctor = Doctor.objects.first()

    def test_get_doctor_list(self):
        """Ensure we can get a list of doctors."""
        url = reverse('home:doctor-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], TEST_DOCTOR_NUM)

        # Test if pagination works
        self.assertNotEqual(response.data['next'], None)

    def test_get_doctor_by_id(self):
        """Ensure we can get one single doctor by id."""
        url = reverse('home:doctor-detail', args=[self.test_doctor.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.test_doctor.id)

    def test_get_doctor_info(self):
        """Ensure we can get a doctor's info by id."""
        url = reverse('home:doctor-info', args=[self.test_doctor.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_doctor_answers(self):
        """Ensure we can get all answers of this doctor."""
        url = reverse('home:doctor-answers', args=[self.test_doctor.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fav_and_unfav_doctor(self):
        """Ensure we can fav a doctor."""
        url = reverse('home:doctor-fav', args=[self.test_doctor.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.patient.favorite_doctors.count(), 0)

        # then unfav the doctor
        url = reverse('home:doctor-unfav', args=[self.test_doctor.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.patient.favorite_doctors.count(), 0)

    def test_get_all_fav_doctors(self):
        """Ensure we can get all of a patient's favorite doctors."""
        # suppose this patient has favved all test doctors
        for doctor in Doctor.objects.all():
            FavoriteDoctor.objects.create(patient=self.patient, doctor=doctor)

        url = reverse('users:patient-fav-doctors')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), TEST_DOCTOR_NUM)
