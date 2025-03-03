from rest_framework.test import APITestCase
from rest_framework import status
from .models import FAQ, ChatbotSession, UserFeedback

class FAQTests(APITestCase):
    def test_create_faq(self):
        data = {'question': 'What is Django?', 'answer': 'Django is a web framework.'}
        response = self.client.post('/faqs/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['question'], 'What is Django?')

class ChatbotSessionTests(APITestCase):
    def test_start_session(self):
        data = {'user_id': 1, 'session_id': 'abcd1234'}
        response = self.client.post('/start-session/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('session_id', response.data)

    def test_send_message(self):
        session_data = {'user_id': 1, 'session_id': 'abcd1234'}
        self.client.post('/start-session/', session_data, format='json')
        message_data = {'session_id': 'abcd1234', 'sender': 'user', 'message': 'Hello, bot!'}
        response = self.client.post('/send-message/', message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sender'], 'user')

class UserFeedbackTests(APITestCase):
    def test_submit_feedback(self):
        session_data = {'user_id': 1, 'session_id': 'abcd1234'}
        self.client.post('/start-session/', session_data, format='json')
        feedback_data = {'session_id': 'abcd1234', 'rating': 5, 'comment': 'Great chatbot!'}
        response = self.client.post('/submit-feedback/', feedback_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)
