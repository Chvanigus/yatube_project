"""Тесты приложения users."""
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus

User = get_user_model()


class AboutUrlsTest(TestCase):
    """Тест urls и доступность шаблонов."""
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='HasNoName')

    def setUp(self):
        """Установка параметров клиентов."""
        self.client = Client()

    def test_author_page(self):
        """Проверяем доступность страницы /author/"""
        response = self.client.get(reverse('about:author'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'about/author.html')

    def test_tech_page(self):
        """Проверяем доступность страницы /tech/"""
        response = self.client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'about/tech.html')
