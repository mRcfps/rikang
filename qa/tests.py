from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import Doctor, Patient, StarredQuestion
from qa.models import Question, Answer, AnswerComment

# Number of questions for test
# Should be larger than PAGE_SIZE
TEST_QUESTION_NUM = 20

# Number of answers for test
TEST_ANSWER_NUM = 5

# Number of comments for test
TEST_COMMENT_NUM = 10


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

    def test_add_and_get_images(self):
        """Ensure we can add images to a question and retrieve them."""
        url = reverse('qa:question-add-image', args=[self.test_question.id])
        with open('test_img.jpg', 'rb') as fp:
            data = {'question': self.test_question.id, 'image': fp}
            response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(Question.objects.first().images.count(), 0)

        url = reverse('qa:question-image-list', args=[self.test_question.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, None)

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

    def test_get_all_starred_questions(self):
        """Ensure we can get all of our starred questions."""
        for question in Question.objects.all():
            StarredQuestion.objects.create(patient=self.patient, question=question)

        url = reverse('users:patient-starred-questions')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), TEST_QUESTION_NUM)


class AnswerTests(APITestCase):
    """Test suite for the answer model."""

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.doctor = Doctor.objects.create(user=self.user, name='test', department='GYN', years=20, title='C')
        self.question = Question.objects.create(title='test', department='GYN', body='test')

        for _ in range(TEST_ANSWER_NUM):
            Answer.objects.create(question=self.question, author=self.doctor)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.test_answer = Answer.objects.first()

    def test_get_answer_list(self):
        """Ensure we can get all answers of one question."""
        url = reverse('qa:answer-list', args=[self.question.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], TEST_ANSWER_NUM)

    def test_get_answer_by_id(self):
        """Ensure we can get an answer by id."""
        url = reverse('qa:answer-detail', args=[self.test_answer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_answer(self):
        """Ensure we can update an answer by id."""
        url = reverse('qa:answer-detail', args=[self.test_answer.id])
        new_data = {
            'question': self.question.id,
            'author': self.doctor.id,
            'diagnosis': 'new_data',
        }
        response = self.client.put(url, new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['diagnosis'], new_data['diagnosis'])

    def test_create_new_answer(self):
        """Ensure we can create a new answer."""
        url = reverse('qa:new-answer', args=[self.question.id])
        data = {'question': self.question.id, 'author': self.doctor.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(Answer.objects.count(), TEST_ANSWER_NUM)

    def test_upvote_answer(self):
        """Ensure we can upvote an answer."""
        url = reverse('qa:answer-upvote', args=[self.test_answer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(Answer.objects.first().upvotes, 0)


class AnswerCommentTests(APITestCase):
    """Test suite for the AnswerComment model."""

    def setUp(self):
        self.doctor_user = User.objects.create_user(username='test_doctor', password='test')
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            name='test_doctor',
            department='GYN',
            years=10,
            title='A'
        )

        self.patient_user = User.objects.create_user(username='test_patient', password='test')
        self.patient = Patient.objects.create(user=self.patient_user, name='test_patient')

        self.client = APIClient()

        self.question = Question.objects.create(
            title='test',
            department='NEO',
            questioner=self.patient,
            body='test'
        )
        self.answer = Answer.objects.create(
            question=self.question,
            author=self.doctor
        )

        for _ in range(TEST_COMMENT_NUM):
            AnswerComment.objects.create(answer=self.answer, replier=self.patient)

    def test_get_comment_list(self):
        """Ensure we can get a list of comments of one answer."""
        url = reverse('qa:answer-comments', args=[self.answer.id])
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], TEST_COMMENT_NUM)

    def test_patient_can_add_new_comment(self):
        """Ensure a patient can create a new comment to an answer."""
        url = reverse('qa:answer-new-comment', args=[self.answer.id])
        data = {
            'answer': self.answer.id,
            'body': 'test',
        }
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(AnswerComment.objects.count(), TEST_COMMENT_NUM)

    def test_doctor_can_add_new_comment(self):
        """Ensure a doctor can create a new comment to an answer."""
        url = reverse('qa:answer-new-comment', args=[self.answer.id])
        data = {
            'answer': self.answer.id,
            'body': 'test',
        }
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(AnswerComment.objects.count(), TEST_COMMENT_NUM)
