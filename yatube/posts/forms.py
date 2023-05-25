"""Формы приложения posts."""

from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Форма создания/редактирования постов."""
    class Meta:
        model = Post
        fields = ('text', 'group')

