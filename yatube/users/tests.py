"""Тесты приложения users."""
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus

User = get_user_model()


class UsersUrlsTest(TestCase):
    """Тест urls и доступность шаблонов."""
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='HasNoName')

    def setUp(self):
        """Установка параметров клиентов."""
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_logout_page(self):
        """Проверяем доступность страницы /logout/"""
        response = self.guest_client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/logged_out.html')

    def test_signup_page(self):
        """Проверяем доступность страницы /signup/"""
        response = self.guest_client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_login_page(self):
        """Проверяем доступность страницы /login/"""
        response = self.guest_client.get(reverse('users:login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_password_change_page(self):
        """Проверяем доступность страницы /password_change/"""
        response = self.authorized_client.get(reverse('users:password_change'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/password_change_form.html')

    def test_password_change_done_page(self):
        """Проверяем доступность страницы /password_change_done/"""
        response = self.authorized_client.get(reverse(
                'users:password_change_done'
        ))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/password_change_done.html')

    def test_password_reset_page(self):
        """Проверяем доступность страницы /password_reset/"""
        response = self.guest_client.get(reverse(
                'users:password_reset'
        ))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/password_reset_form.html')

    def test_password_reset_done_page(self):
        """Проверяем доступность страницы /password_reset/done/"""
        response = self.guest_client.get(reverse(
                'users:password_reset_done'
        ))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/password_reset_done.html')

    def test_password_reset_confirm_page(self):
        """Проверяем доступность страницы /reset/<uidb64>/<token>/"""
        uidb64 = 'valid_uidb64'
        token = 'valid_token'
        response = self.guest_client.get(reverse(
                'users:password_reset_confirm',
                args=[uidb64, token]
        ))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/password_reset_confirm.html')

    def test_password_reset_complete_page(self):
        """Проверяем доступность страницы /reset/done/"""
        response = self.guest_client.get(reverse(
                'users:password_reset_complete'
        ))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/password_reset_complete.html')
