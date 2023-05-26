"""Views приложения posts."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, \
    RedirectView, UpdateView

from .forms import CommentForm, PostForm
from .models import Comments, Follow, Group, Post, User


class IndexView(ListView):
    """Главная страница."""
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 10
    context_object_name = 'post_list'


class GroupPostsView(ListView):
    """Посты по группам."""
    model = Post
    template_name = 'posts/group_list.html'
    paginate_by = 10
    context_object_name = 'post_list'

    def get_queryset(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return Post.objects.filter(group=group)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        context['group'] = group
        return context


class ProfileView(ListView):
    """Профайл пользователя."""
    model = Post
    template_name = 'posts/profile.html'
    paginate_by = 10
    context_object_name = 'post_list'

    def get_queryset(self):
        author = User.objects.get(username=self.kwargs['username'])
        return Post.objects.filter(author=author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        author = User.objects.get(username=self.kwargs['username'])

        following = Follow.objects.filter(user=user, author=author).exists()

        context['post_count'] = self.get_queryset().count()
        context['author'] = author
        context['following'] = following
        return context


class PostDetailView(DetailView):
    """Страница детального просмотра поста."""
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comments.objects.filter(post_id=self.object.pk)
        posts_count = Post.objects.filter(author=self.object.author).count()

        context['comments'] = comments
        context['form'] = CommentForm()
        context['posts_count'] = posts_count
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Страница создания поста."""
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context

    def get_success_url(self):
        return reverse_lazy(
                'posts:profile',
                kwargs={'username': self.request.user.username}
        )


class PostEditView(LoginRequiredMixin, UpdateView):
    """Страница редактирования поста."""
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect('posts:post_detail', pk=post.pk)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect(
                'posts:profile',
                username=self.request.user.username
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['is_edit'] = True
        return context


class AddCommentFormView(LoginRequiredMixin, FormView):
    """Добавление комментариев."""
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = Post.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class FollowView(LoginRequiredMixin, ListView):
    """Страница подписок пользователя"""
    template_name = 'posts/follow.html'
    model = Post
    paginate_by = 10

    def get_queryset(self):
        follows = Follow.objects.filter(user_id=self.request.user)
        authors = [follow.author for follow in follows]
        return Post.objects.filter(author_id__in=authors)


class FollowAuthorView(LoginRequiredMixin, RedirectView):
    """Подписка на автора."""

    def get_redirect_url(self, *args, **kwargs):
        author = get_object_or_404(User, username=self.kwargs['username'])
        follow = Follow.objects.get_or_create(
                user_id=self.request.user.id,
                author_id=author.id
        )
        print(follow)
        return reverse('posts:profile', kwargs={'username': author.username})


class UnfollowAuthorView(LoginRequiredMixin, RedirectView):
    """Отписка от автора."""
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        author = get_object_or_404(User, username=self.kwargs['username'])
        Follow.objects.filter(user=self.request.user, author=author).delete()
        return reverse('posts:profile', kwargs={'username': author.username})
