from django.test import TestCase
from rest_framework.test import APIClient

from .models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='mariorossi@gmail.com', username='Mario Rossi')

    def test_user_to_str(self):
        """Tests that the model is represented in string as expected."""
        user = User.objects.get(id=1)
        actual_repr = str(user)
        expected_repr = 'Mario Rossi'
        self.assertEquals(expected_repr, actual_repr)


class UserViewsTest(TestCase):
    def setUp(self):
        User.objects.create(email='mariorossi@gmail.com', username='Mario Rossi')
        User.objects.create(email='lucaverdi@gmail.com', username='Luca Verdi')
        User.objects.create(email='paolobianchi@gmail.com', username='Paolo Bianchi')
        self.client = APIClient()

    def test_get_users(self):
        """Tests the correct response of the endpoint which allows to obtain the list of all users."""
        response = self.client.get('/users/')
        actual_data = response.content
        expected_data = (b'[{"id":12,"email":"mariorossi@gmail.com","username":"Mario Rossi"},{"id":13,'
                         b'"email":"lucaverdi@gmail.com","username":"Luca Verdi"},{"id":14,'
                         b'"email":"paolobianchi@gmail.com","username":"Paolo Bianchi"}]')

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, actual_data)

    def test_retrieve_user(self):
        """Tests the correct response of the endpoint that allows you to find a user through his id."""
        id_user_to_retrieve = User.objects.get(email='mariorossi@gmail.com').id
        response = self.client.get(f'/users/{id_user_to_retrieve}/')
        actual_data = response.content
        expected_data = b'{"id":15,"email":"mariorossi@gmail.com","username":"Mario Rossi"}'

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, actual_data)

    def test_create_users(self):
        """Tests the correct response of the endpoint which allows the creation of a new user."""
        response = self.client.post('/users/', data={'email': 'paologialli@gmail.com', 'username': 'Paolo Gialli'})
        actual_data = response.content
        expected_data = b'{"id":5,"email":"paologialli@gmail.com","username":"Paolo Gialli"}'

        self.assertEqual(201, response.status_code)
        self.assertEqual(expected_data, actual_data)

    def test_create_users_email_not_valid(self):
        """Tests the correct response of the endpoint when an invalid email is provided."""
        response = self.client.post('/users/', data={'email': 'paologialligmail.com', 'username': 'Paolo Gialli'})
        self.assertEqual(400, response.status_code)

    def test_delete_users(self):
        """Tests the correct response of the endpoint that allows to delete a user."""
        id_user_to_delete = User.objects.get(email='mariorossi@gmail.com').id
        response = self.client.delete(f'/users/{id_user_to_delete}/')
        self.assertEqual(204, response.status_code)

    def test_update_users(self):
        """Tests the correct response of the endpoint that allows to update a user."""
        id_user_to_update = User.objects.get(email='mariorossi@gmail.com').id
        response = self.client.put(f'/users/{id_user_to_update}/', data={'email': 'rossi@gmail.com', 'username': 'Mario Rossi'})
        actual_data = response.content
        expected_data = b'{"id":18,"email":"rossi@gmail.com","username":"Mario Rossi"}'

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, actual_data)
