"""Views приложения Posts."""
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    """Функция представления главной страницы"""
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': 'Последние новости'
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Посты по группам."""
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
        'title': f'Записи сообщества {group.title}'
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Страница с информацией о пользователе."""
    user = User.objects.get(username=username)

    post_list = Post.objects.filter(author=user).order_by('-pub_date')
    post_count = post_list.count()

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': f'Профайл пользователя {username}',
        'username': username,
        'post_count': post_count
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Страница детального просмотра поста."""
    post = Post.objects.get(pk=post_id)
    post_count = Post.objects.filter(author=post.author).order_by(
            '-pub_date').count()

    context = {
        'post': post,
        'post_count': post_count
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Страница создания постов."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user.username)
    else:
        form = PostForm()

    context = {
        'form': form,
        'title': 'Создание записи',
        'is_edit': False
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    """Страница редактирования поста."""
    post = Post.objects.get(pk=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('posts:profile', username=request.user.username)
    else:
        form = PostForm(instance=post)

    context = {
        'title': 'Редактирование записи',
        'is_edit': True,
        'form': form,
        'pk': post_id
    }

    return render(request, 'posts/create_post.html', context)
