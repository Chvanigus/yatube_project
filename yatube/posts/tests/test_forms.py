"""Тесты форм приложения posts."""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostsCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='HasNoName')
        cls.group = Group.objects.create(
                title='Тестовая группа',
                slug='test-group',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_creation_form(self):
        """Проверяем, что форма создаёт новую запись."""

        form_data = {
            'text': 'Test post',
            'group': self.group.id,
        }

        response = self.authorized_client.post(
                reverse('posts:post_create'),
                data=form_data,
                follow=True
        )

        self.assertEqual(Post.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.text, 'Test post')
        self.assertEqual(new_post.group, self.group)
        self.assertEqual(new_post.author, self.user)

        self.assertRedirects(response, reverse('posts:profile',
                                               args=[self.user.username]))

    def test_post_edit_form(self):
        """Проверяем, что форма изменяет существующую запись."""

        post = Post.objects.create(
                text='Original post',
                group=self.group,
                author=self.user
        )

        form_data = {
            'text': 'Updated post',
            'group': self.group.id,
        }

        response = self.authorized_client.post(
                reverse('posts:post_edit', args=[post.id]),
                data=form_data,
                follow=True
        )

        self.assertEqual(Post.objects.count(), 1)
        updated_post = Post.objects.first()
        self.assertEqual(updated_post.text, 'Updated post')
        self.assertEqual(updated_post.group, self.group)
        self.assertEqual(updated_post.author, self.user)

        self.assertRedirects(response, reverse('posts:profile',
                                               args=[self.user.username]))
