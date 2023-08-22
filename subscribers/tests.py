from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from .models import Subscriber


class SubscriberModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Subscriber.objects.create(email='mariorossi@gmail.com', username='Mario Rossi')

    def test_subscriber_to_str(self):
        """Tests that the model is represented in string as expected."""
        subscriber = Subscriber.objects.get(email='mariorossi@gmail.com')
        actual_repr = str(subscriber)
        expected_repr = 'Mario Rossi'
        self.assertEquals(expected_repr, actual_repr)


class SubscribersViewsTest(TestCase):
    def setUp(self):
        Subscriber.objects.create(email='mariorossi@gmail.com', username='Mario Rossi')
        Subscriber.objects.create(email='lucaverdi@gmail.com', username='Luca Verdi')
        Subscriber.objects.create(email='paolobianchi@gmail.com', username='Paolo Bianchi')
        User.objects.create_superuser(username='user', password='pass')

        self.client = APIClient()
        self.client.login(username='user', password='pass')

    def test_get_subscribers(self):
        """Tests the correct response of the endpoint which allows to obtain the list of all subscribers."""
        response = self.client.get('/subscribers/')
        actual_data = response.content
        expected_data = (b'[{"id":36,"email":"mariorossi@gmail.com","username":"Mario Rossi"},{"id":37,'
                         b'"email":"lucaverdi@gmail.com","username":"Luca Verdi"},{"id":38,'
                         b'"email":"paolobianchi@gmail.com","username":"Paolo Bianchi"}]')

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, actual_data)

    def test_retrieve_subscriber(self):
        """Tests the correct response of the endpoint that allows you to find a subscriber through his id."""
        id_sub_to_retrieve = Subscriber.objects.get(email='mariorossi@gmail.com').id
        response = self.client.get(f'/subscribers/{id_sub_to_retrieve}/')
        actual_data = response.content
        expected_data = b'{"id":39,"email":"mariorossi@gmail.com","username":"Mario Rossi"}'

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, actual_data)

    def test_create_subscribers(self):
        """Tests the correct response of the endpoint which allows the creation of a new subscriber."""
        response = self.client.post('/subscribers/', data={'email': 'paologialli@gmail.com', 'username': 'Paolo Gialli'})
        actual_data = response.content
        expected_data = b'{"id":29,"email":"paologialli@gmail.com","username":"Paolo Gialli"}'

        self.assertEqual(201, response.status_code)
        self.assertEqual(expected_data, actual_data)

    def test_create_subscribers_email_not_valid(self):
        """Tests the correct response of the endpoint when an invalid email is provided."""
        response = self.client.post('/subscribers/', data={'email': 'paologialligmail.com', 'username': 'Paolo Gialli'})
        self.assertEqual(400, response.status_code)

    def test_delete_subscribers(self):
        """Tests the correct response of the endpoint that allows to delete a subscriber."""
        id_sub_to_delete = Subscriber.objects.get(email='mariorossi@gmail.com').id
        response = self.client.delete(f'/subscribers/{id_sub_to_delete}/')
        self.assertEqual(204, response.status_code)

    def test_update_subscribers(self):
        """Tests the correct response of the endpoint that allows to update a subscriber."""
        id_sub_to_update = Subscriber.objects.get(email='mariorossi@gmail.com').id
        response = self.client.put(f'/subscribers/{id_sub_to_update}/', data={'email': 'rossi@gmail.com', 'username': 'Mario Rossi'})
        actual_data = response.content
        expected_data = b'{"id":42,"email":"rossi@gmail.com","username":"Mario Rossi"}'

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, actual_data)
