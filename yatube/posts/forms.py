"""Формы приложения posts."""

from django import forms
from .models import Post, Comments


class PostForm(forms.ModelForm):
    """Форма создания/редактирования постов."""
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    """Форма создания комментария."""
    class Meta:
        model = Comments
        fields = ('text',)
