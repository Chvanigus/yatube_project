"""Тесты модели приложения Posts."""
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Подготовка данных."""
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
                title='Тестовая группа',
                slug='Тестовый слаг',
                description='Тестовое описание',
        )
        cls.post = Post.objects.create(
                author=cls.user,
                text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.assertEqual(str(self.user), self.user.username)
        self.assertEqual(str(self.group), self.group.title)
        self.assertEqual(str(self.post), self.post.text)

    def test_verbose_name(self):
        post = Post.objects.get(id=self.post.id)
        field_verbose_names = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, verbose_name in field_verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                        post._meta.get_field(field).verbose_name,
                        verbose_name
                )

    def test_help_text(self):
        post = Post.objects.get(id=self.post.id)
        field_help_texts = {
            'text': 'Введите текст поста',
            'pub_date': '',
            'author': '',
            'group': 'Группа, к которой относится пост',
        }
        for field, help_text in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                        post._meta.get_field(field).help_text,
                        help_text
                )
