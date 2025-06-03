from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .views import chatbot_view

class ChatbotViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('chatbot')

    def test_get_request_renders_chat_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat.html')
        self.assertIn('chat_history', response.context)
        self.assertIsInstance(response.context['chat_history'], list)

    @patch('home.views.groq_client.chat.completions.create')
    def test_post_request_updates_chat_history(self, mock_groq):
        mock_groq.return_value.choices = [
            type('obj', (object,), {
                'message': type('msg', (object,), {'content': 'Hello!'})
            })()
        ]

        response = self.client.post(self.url, {'message': 'Hi'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello!')

        session = self.client.session
        self.assertIn('chat_history', session)
        self.assertEqual(len(session['chat_history']), 2)
        self.assertEqual(session['chat_history'][0]['sender'], 'user')
        self.assertEqual(session['chat_history'][1]['sender'], 'bot')

    @patch('home.views.groq_client.chat.completions.create', side_effect=Exception("API error"))
    def test_post_request_handles_groq_exception(self, mock_groq):
        response = self.client.post(self.url, {'message': 'Hi'})
        self.assertContains(response, '🚨 Bot failed to respond.')

        session = self.client.session
        self.assertEqual(len(session['chat_history']), 2)
        self.assertEqual(session['chat_history'][1]['message'], '🚨 Bot failed to respond.')
