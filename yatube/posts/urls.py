"""Urls приложения Posts."""

from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path(
            '',
            views.IndexView.as_view(),
            name='index'
    ),
    path(
            'group/<slug:slug>/',
            views.GroupPostsView.as_view(),
            name='group_list'
    ),
    path(
            'profile/<str:username>/',
            views.ProfileView.as_view(),
            name='profile'
    ),
    path(
            'posts/<int:pk>/',
            views.PostDetailView.as_view(),
            name='post_detail'
    ),
    path(
            'create/',
            views.PostCreateView.as_view(),
            name='post_create'
    ),
    path(
            'posts/<int:pk>/edit/',
            views.PostEditView.as_view(),
            name='post_edit'
    ),
    path(
            'posts/<int:pk>/comment/',
            views.AddCommentFormView.as_view(),
            name='add_comment'
    ),
]
