"""Модели приложения Posts."""
from django.contrib.auth import get_user_model
from django.db import models
from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    """ Модель групп"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, db_index=True, verbose_name="URL")
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(CreatedModel):
    """Модель постов"""
    text = models.TextField(
            'Текст поста',
            help_text='Введите текст поста'
    )
    author = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='posts',
            verbose_name='Автор'
    )
    group = models.ForeignKey(
            Group,
            on_delete=models.SET_NULL,
            related_name='posts',
            blank=True,
            null=True,
            verbose_name='Группа',
            help_text='Группа, к которой относится пост'
    )
    image = models.ImageField(
            'Картинка',
            upload_to='posts/',
            blank=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comments(CreatedModel):
    """Модель комментариев."""
    post = models.ForeignKey(
            Post,
            verbose_name='Пост',
            help_text='Ссылка на пост',
            on_delete=models.CASCADE,
            related_name='comments'
    )
    author = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='comments',
            verbose_name='Автор'
    )
    text = models.CharField(
            max_length=350,
            verbose_name='Текст комментария',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
