"""Views приложения core"""
from django.shortcuts import render


def page_not_found(request, exception):
    """Страница 404."""
    # Переменная exception содержит отладочную информацию;
    # выводить её в шаблон пользовательской страницы 404 мы не станем
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def csrf_failure(request, reason=''):
    """Страница 403 при отсутствии csrf токена."""
    return render(request, 'core/403csrf.html')


def server_error(request):
    """Страница 500."""
    return render(request, 'core/500.html', status=500)


def permission_denied(request, exception):
    """Страница 403."""
    return render(request, 'core/403.html', status=403)
