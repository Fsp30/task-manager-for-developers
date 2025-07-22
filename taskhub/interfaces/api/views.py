from django.shortcuts import render
from django.http import HttpResponse
from social_django.models import UserSocialAuth
from ...core.models import Task

from django.views.decorators.http import require_POST


def home(request):
    if request.user.is_authenticated:
        try:
            github_login = request.user.social_auth.get(provider='github')
            token = github_login.extra_data['access_token']
            username = github_login.extra_data['login']
        except UserSocialAuth.DoesNotExist:
            token = None
            username = request.user.username
        return HttpResponse(f"""
            <h1>Bem-vindo, {username}!</h1>
            <p>Token do GitHub: {token}</p>
            <a href='/logout/'>
                <button>Logout</button>
            </a>
        """)
    else:
        return HttpResponse("""
            <h1>Test dev's</h1>
            <a href='/auth/login/github/'>
                <button>Login com GitHub</button>
            </a>
        """)

@require_POST
def create_task(request):
    title = request.POST.get('title', 'Default task')
    Task(title=title).save()
    return HttpResponse('success, create task')
