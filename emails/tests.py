from unittest.mock import patch

from django.test import TestCase
from django.core import mail
from django.conf import settings
from rest_framework.test import APIClient

from subscribers.models import Subscriber


class EmailsTestCase(TestCase):
    def setUp(self):
        settings.EMAIL_HOST = 'localhost'
        settings.EMAIL_HOST_USER = '********'
        settings.EMAIL_HOST_PASSWORD = '*******'
        settings.EMAIL_PORT = '8025'

        Subscriber.objects.create(email='mariorossi@gmail.com', username='Mario Rossi')
        Subscriber.objects.create(email='lucaverdi@gmail.com', username='Luca Verdi')
        Subscriber.objects.create(email='paolobianchi@gmail.com', username='Paolo Bianchi')

        self.client = APIClient()

    def test_email_all_subscribers_ok(self):
        """Tests the correct response of the endpoint when sending emails is successful and that the email is sent to
        all subscribers."""
        response = self.client.post('/emails/send_to_all/', data={'subject': 'test_subject', 'message': 'test_message'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"msg":"Emails successfully sent"}', response.content)

        actual = mail.outbox[0].recipients()
        expected = ['mariorossi@gmail.com', 'lucaverdi@gmail.com', 'paolobianchi@gmail.com']
        self.assertEqual(expected, actual, "Expected different recipients list.")

    @patch('emails.views.send_mail')
    def test_email_all_subscribers_error_sending_email(self, mock_send_mail):
        """Tests the correct response of the endpoint when sending emails fails."""
        mock_send_mail.return_value = 0
        response = self.client.post('/emails/send_to_all/', data={'subject': 'test_subject', 'message': 'test_message'})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'{"msg":"Error sending email"}', response.content)

    def test_email_all_subscribers_missing_subject(self):
        """Tests the correct response of the endpoint when subject is missing."""
        response = self.client.post('/emails/send_to_all/', data={'recipients': ['test@gmail.com'], 'message': 'test_message'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"msg":"Emails successfully sent"}', response.content)

        actual = mail.outbox[0].subject
        expected = ''
        self.assertEqual(actual, expected, 'Expected that subject must be an empty string.')

    def test_email_all_subscribers_missing_message(self):
        """Tests the correct response of the endpoint when message is missing."""
        response = self.client.post('/emails/send_to_all/', data={'subject': 'test_subject'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"msg":"Emails successfully sent"}', response.content)

        actual = mail.outbox[0].body
        expected = ''
        self.assertEqual(actual, expected, 'Expected that the body of the message must be an empty string.')

    def test_email_specific_subscribers_ok(self):
        """Tests the correct response of the endpoint when sending emails is successful and that the email is sent to
        the correct subscribers."""
        response = self.client.post('/emails/send/', data={'recipients': [22, 23], 'subject': 'test_subject', 'message': 'test_message'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"msg":"Emails successfully sent"}', response.content)

        actual = mail.outbox[0].recipients()
        expected = ['mariorossi@gmail.com', 'lucaverdi@gmail.com']
        self.assertEqual(actual, expected, "Expected different recipients list.")

    def test_email_specific_subscribers_missing_recipients(self):
        """Tests the correct response of the endpoint when recipients is missing."""
        response = self.client.post('/emails/send/', data={'subject': 'test_subject', 'message': 'test_message'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'{"msg":"Recipient list required"}', response.content)

    def test_email_specific_subscribers_emails_partially_sent(self):
        """Tests the correct response of the endpoint when emails are partially sent."""
        response = self.client.post('/emails/send/', data={'recipients': [12, 13], 'subject': 'test_subject', 'message': 'test_message'})
        self.assertEqual(response.status_code, 206)
        self.assertIn(b'{"msg":"Emails partially sent, subscribers not found: [\'12\']"}', response.content)

    @patch('emails.views.send_mail')
    def test_email_specific_subscribers_error_sending_email(self, mock_send_mail):
        """Tests the correct response of the endpoint when sending emails fails."""
        mock_send_mail.return_value = 0
        response = self.client.post('/emails/send_to_all/', data={'recipients': [16], 'subject': 'test_subject', 'message': 'test_message'})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'{"msg":"Error sending email"}', response.content)
