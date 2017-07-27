from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Feedback


class FeedbackTests(APITestCase):
    """Test suite for the feedback model."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.user)

    def test_send_feedback(self):
        """Ensure we can send a feedback to the server."""
        url = reverse('feedback:send-feedback')
        data = {'body': 'This is a test.'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feedback.objects.count(), 1)
