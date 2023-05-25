"""Тесты urls приложения posts."""
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus

from ..models import Group, Post

User = get_user_model()


class PostsUrlsTest(TestCase):
    """Тест urls и доступность шаблонов."""
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='HasNoName')
        cls.group = Group.objects.create(
                title='Тестовая группа',
                slug='test-group',
        )
        cls.post = Post.objects.create(
                author=cls.user,
                text='Тестовый пост',
                group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_page(self):
        """Проверяем доступность страницы /"""
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_list_page(self):
        """Проверяем доступность страницы /group/test-group/"""
        response = self.guest_client.get(reverse(
                'posts:group_list',
                args=[self.group.slug]
        ))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_page(self):
        """Проверяем доступность страницы /profile/HasNoName/"""
        response = self.guest_client.get(reverse(
                'posts:profile',
                args=[self.user.username]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_page(self):
        """Проверяем доступность страницы /posts/{post_id}/"""
        response = self.guest_client.get(reverse(
                'posts:post_detail',
                args=[self.post.id]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_page(self):
        """Проверяем доступность страницы /posts/{post_id}/edit/"""
        response = self.authorized_client.get(reverse(
                'posts:post_edit',
                args=[self.post.id]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_page(self):
        """Проверяем доступность страницы /create/"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_page(self):
        """Проверяем доступность несуществующей страницы /unxexisting_page/"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
