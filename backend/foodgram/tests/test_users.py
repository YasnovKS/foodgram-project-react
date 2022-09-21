from http import HTTPStatus

from django.test import Client, TestCase

from users.models import User


class TestUsersView(TestCase):
    '''Testing users module (creating, authorization, editing)'''
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.test_user = User.objects.create_user(username='Kirill',
                                                 password='123qweasdzxc1',
                                                 email='1@1.ru',
                                                 first_name='Kirill',
                                                 last_name='Yasnov'
                                                 )

    def setUp(self) -> None:
        super().setUp()

        self.client = Client()
        self.client.force_login(self.test_user)

    def test_create_user_with_valid_data(self):
        users_count = User.objects.all().count()

        data = {
            "username": "Vasia",
            "password": "vasia123qwerty",
            "email": "vasia@mail.ru",
            "first_name": "Vasily",
            "last_name": "Vasin"
        }

        endpoint = '/api/users/'

        response = self.client.post(endpoint, data)

        # checking that we got status_code == 'Created' in response
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        # checking that we got +1 user after request
        self.assertEqual(User.objects.all().count(), users_count + 1)

    def test_create_user_with_invalid_data(self):
        '''Testing that users cant be created with invalid data'''
        users_count = User.objects.all().count()

        data = {
            "username": "Vasia",
            "password": "vasia123qwerty",
            "email": "vasia@mail.ru",
            "first_name": "Vasily",
            "last_name": "Vasin"
        }

        for key in data.keys():
            with self.subTest(value=key):
                data[key] = ""
                endpoint = '/api/users/'

                response = self.client.post(endpoint, data)

                # checking that we got status_code == 'Bad Request' in response
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

                # checking that quantity of users was not changed
                self.assertEqual(User.objects.all().count(), users_count)
