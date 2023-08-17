from unittest.mock import patch

from django.test import TestCase
from django.core import mail
from django.conf import settings
from rest_framework.test import RequestsClient


class EmailsTestCase(TestCase):
    def setUp(self):
        settings.EMAIL_HOST = 'localhost'
        settings.EMAIL_HOST_USER = '********'
        settings.EMAIL_HOST_PASSWORD = '*******'
        settings.EMAIL_PORT = '8025'
        self.client = RequestsClient()

    def test_post_emails_send_ok(self):
        """Tests the correct response of the endpoint when sending emails is successful."""
        response = self.client.post('http://testserver/emails/send/', json={'recipients': ['test@gmail.com'], 'subject': 'test_subject', 'message': 'test_message'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"msg":"Emails successfully sent"}', response.content)

    def test_post_emails_send_missing_recipients(self):
        """Tests the correct response of the endpoint when recipients is missing."""
        response = self.client.post('http://testserver/emails/send/', json={'subject': 'test_subject', 'message': 'test_message'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'{"msg":"Recipient list required"}', response.content)

    def test_post_emails_send_missing_subject(self):
        """Tests the correct response of the endpoint when subject is missing."""
        response = self.client.post('http://testserver/emails/send/', json={'recipients': ['test@gmail.com'], 'message': 'test_message'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"msg":"Emails successfully sent"}', response.content)

        actual = mail.outbox[0].subject
        expected = ''
        self.assertEqual(actual, expected, 'Expected that subject must be an empty string.')

    def test_post_emails_send_missing_message(self):
        """Tests the correct response of the endpoint when message is missing."""
        response = self.client.post('http://testserver/emails/send/',
                                    json={'recipients': ['test@gmail.com'], 'subject': 'test_subject'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"msg":"Emails successfully sent"}', response.content)

        actual = mail.outbox[0].body
        expected = ''
        self.assertEqual(actual, expected, 'Expected that the body of the message must be an empty string.')

    @patch('emails.views.send_mail')
    def test_post_emails_send_error_sending_email(self, mock_send_mail):
        """Tests the correct response of the endpoint when sending emails fails."""
        mock_send_mail.return_value = 0
        response = self.client.post('http://testserver/emails/send/', json={'recipients': ['test@gmail.com'], 'subject': 'test_subject', 'message': 'test_message'})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'{"msg":"Error sending email"}', response.content)
