from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime
import json

class ChatViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.valid_payload_without_sys_msg = {
            'message': 'Hi there',
            # 'session': self.session.id,
            'history': [],
        }
        self.valid_payload = {
            'message': 'What is the weather like today?',
            # 'session': self.session.id,
            'history': [{'role': 'system', 'message': 'You are a helpful assistant.', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}],
        }
        self.invalid_payload = {
            'message': 'What is the weather like today?',
            # 'session': 123456,
            'history': 'System: You are a helpful assistant.',
        }

    def test_create_chat(self):
        response = self.client.post('/api/chat/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_chat_without_sys_msg(self):
        response = self.client.post('/api/chat/', self.valid_payload_without_sys_msg, format='json')
        # Define the items you expect to find in the history
        expected_items = [
            {
                "role": "system",
                "message": "You are a helpful assistant.",
            }
        ]
        # Extract the 'user' and 'message' fields from each item in the history
        actual_items = [{'role': item['role'], 'message': item['message']} for item in response.data['history']]

        # Check that each expected item is in the actual history
        for expected_item in expected_items:
            self.assertIn(expected_item, actual_items)
        
        self.assertEqual(response.status_code, 201)
        
    # def test_create_chat_invalid_session(self):
    #     response = self.client.post('/api/chat/', self.invalid_payload, format='json')
    #     self.assertEqual(response.status_code, 404)

def format_json_data(response_data):
    return json.dumps(response_data, indent=4)
