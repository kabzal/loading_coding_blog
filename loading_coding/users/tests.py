from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterUserTestCase(TestCase):
    fixtures = ["all_data.json"]

    def setUp(self):
        self.data = {
            'username': 'useless_user',
            'email': 'useless@mail.com',
            'first_name': 'Бесполезник',
            'last_name': 'Бесполезный',
            'password1': 'Useless1password2',
            'password2': 'Useless1password2',
        }

    def test_form_registration_get(self):
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_success(self):
        user_model = get_user_model()
        path = reverse('users:register')
        response = self.client.post(path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())

    def test_user_registration_password_error(self):
        self.data['password2'] = 'Useful1password2'
        path = reverse('users:register')
        response = self.client.post(path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Введенные пароли не совпадают.", html=True)

    def test_user_registration_exists_error(self):
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'])

        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Пользователь с таким именем уже существует")
