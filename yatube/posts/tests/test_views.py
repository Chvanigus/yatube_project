"""Тесты views приложения posts."""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post


User = get_user_model()


class PostsContextViewsTest(TestCase):
    """Тесты views."""

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

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        pages_templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:post_detail', kwargs={
                'post_id': 1}): 'posts/post_detail.html',
            reverse('posts:profile', kwargs={
                'username': 'HasNoName'}): 'posts/profile.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}):
                'posts/create_post.html'
        }

        for reverse_name, template in pages_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_detail_context(self):
        """Проверяем контекст во view-функции post_detail"""
        response = self.guest_client.get(
                reverse('posts:post_detail', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)

    def test_profile_context(self):
        """Проверяем контекст во view-функции profile"""
        response = self.guest_client.get(
                reverse('posts:profile',
                        kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['username'], self.user.username)
        self.assertEqual(response.context['post_count'], 1)

    def test_group_posts_context(self):
        """Проверяем контекст во view-функции group_posts"""
        response = self.guest_client.get(
                reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['group'], self.group)
        self.assertQuerysetEqual(response.context['page_obj'], [self.post])

    def test_post_create_context(self):
        """Проверяем контекст во view-функции post_create"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertEqual(response.context['is_edit'], False)

    def test_post_edit_context(self):
        """Проверяем контекст во view-функции post_edit"""
        response = self.authorized_client.get(
                reverse('posts:post_edit', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertEqual(response.context['is_edit'], True)
        self.assertEqual(response.context['pk'], self.post.pk)


class PostsPaginatorTest(TestCase):
    """Тесты пагинации"""

    def setUp(self):
        """Создание постов и группы"""
        self.user = User.objects.create_user(username='HasNoName')
        self.group = Group.objects.create(
                title='Test Group',
                slug='test-group',
        )
        for i in range(15):
            Post.objects.create(
                    text=f'Test Post {i + 1}',
                    pub_date='2023-01-01',
                    author=self.user,
                    group=self.group
            )

    def test_first_page_index_pagination(self):
        """На первой странице index содержится 10 записей."""
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_index_pagination(self):
        """На второй странице index содержится 5 записей."""
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_first_page_group_posts_pagination(self):
        """На первой странице постов по группе содержится 10 постов."""
        response = self.client.get(
                reverse('posts:group_list', kwargs={'slug': self.group.slug}))

        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_group_posts_pagination(self):
        """На второй странице постов по группе содержится 5 постов."""
        response = self.client.get(
                reverse('posts:group_list',
                        kwargs={'slug': self.group.slug})
                + '?page=2')

        self.assertEqual(len(response.context['page_obj']), 5)

    def test_first_page_profile_pagination(self):
        """На первой странице профиля содержится 10 постов."""
        response = self.client.get(
                reverse('posts:profile',
                        kwargs={'username': self.user.username}))

        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_profile_pagination(self):
        """На второй странице профиля содержится 5 постов."""
        response = self.client.get(
                reverse('posts:profile',
                        kwargs={'username': self.user.username})
                + '?page=2')

        self.assertEqual(len(response.context['page_obj']), 5)


class PostsCreateTest(TestCase):
    """Тест на создание поста"""

    def setUp(self):
        """Установка данных."""
        self.user = User.objects.create_user(username='HasNoName')
        self.group = Group.objects.create(
                title='Test Group',
                slug='test-group')

    def test_post_create(self):
        """Проверка на создание поста.
        Если при создании поста указать группу, то этот пост появляется
        на главной странице сайта, на странице выбранной группы,
        в профайле пользователя.
        Проверка на то, что этот пост не попал в группу, для которой не был
        предназначен."""
        self.client.force_login(user=self.user)

        response = self.client.post(reverse('posts:post_create'), {
            'text': 'Test post',
            'group': self.group.pk,
        })

        self.assertRedirects(
                response, reverse('posts:profile',
                                  kwargs={'username': self.user.username}))

        response = self.client.get(reverse('posts:index'))
        self.assertContains(response, 'Test post')

        response = self.client.get(
                reverse('posts:group_list',
                        kwargs={'slug': self.group.slug}))
        self.assertContains(response, 'Test post')

        response = self.client.get(
                reverse('posts:profile',
                        kwargs={'username': self.user.username}))
        self.assertContains(response, 'Test post')

        other_group = Group.objects.create(
                title='Other Group',
                slug='other-group')
        response = self.client.get(
                reverse('posts:group_list',
                        kwargs={'slug': other_group.slug}))
        self.assertNotContains(response, 'Test post')
