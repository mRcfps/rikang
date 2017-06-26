from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from home.models import Post, Hospital

# Number of news for test
# Should be larger than PAGE_SIZE
TEST_POST_NUM = 20

# Number of hospitals for test
# Should be larger than PAGE_SIZE
TEST_HOSPITAL_NUM = 20


class PostTests(APITestCase):
    """Test suite for the post model."""

    def setUp(self):
        """Initialize several posts to play with."""
        for index in range(TEST_POST_NUM):
            content = 'Test {}'.format(index)
            Post.objects.create(title=content, body=content)

        self.client = APIClient()
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


class HospitalTests(APITestCase):
    """Test suite for the hospital model."""

    def setUp(self):
        """Initialize several hospitals to play with."""
        for _ in range(TEST_HOSPITAL_NUM):
            Hospital.objects.create(name='test', rank='3A', phone=123456)

        self.client = APIClient()
        self.test_hospital = Hospital.objects.first()

    def test_get_Hospital_list(self):
        """Ensure we can get a list of hospitals."""
        url = reverse('home:hospital-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], TEST_HOSPITAL_NUM)

        # Test if pagination works
        self.assertNotEqual(response.data['next'], None)

    def test_get_Hospital_by_id(self):
        """Ensure we can get one single hospital by id."""
        url = reverse('home:hospital-detail', args=[self.test_hospital.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.test_hospital.id)
