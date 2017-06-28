from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import Patient
from qa.models import Question, Answer

# Number of questions for test
# Should be larger than PAGE_SIZE
TEST_QUESTION_NUM = 20


class QuestionTests(APITestCase):
    """Test suite for the question model."""

    def setUp(self):
        """Initialize several questions to play with."""
        self.user = User.objects.create_user(username='test', password='test')
        self.patient = Patient.objects.create(user=self.user)

        for _ in range(TEST_QUESTION_NUM):
            Question.objects.create(
                title='test',
                department='NEO',
                questioner=self.patient,
                body='text'
            )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.test_question = Question.objects.first()

    def test_get_question_list(self):
        """Ensure we can get a list of questions."""
        url = reverse('qa:question-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], TEST_QUESTION_NUM)

        # Test if pagination works
        self.assertNotEqual(response.data['next'], None)

    def test_get_question_by_id(self):
        """Ensure we can get one single question by id."""
        url = reverse('qa:question-detail', args=[self.test_question.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.test_question.id)

    def test_create_new_question(self):
        """Ensure we can create a new question."""
        url = reverse('qa:new-question')
        data = {
            'title': 'new question',
            'department': 'PNE',
            'body': 'new',
            'questioner': self.patient.id,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(Question.objects.count(), TEST_QUESTION_NUM)

    def test_update_question(self):
        """Ensure we can edit an existed question."""
        url = reverse('qa:question-detail', args=[self.test_question.id])
        new_data = {
            'title': 'new question',
            'department': 'NEO',
            'questioner': self.patient.id,
            'body': 'new question body',
        }
        response = self.client.put(url, new_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Question.objects.first().title, new_data['title'])

    def test_star_question(self):
        """Ensure we can star a question."""
        url = reverse('qa:star-question', args=[self.test_question.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(Question.objects.first().stars, 0)
        self.assertNotEqual(self.patient.starred_questions.count(), 0)
