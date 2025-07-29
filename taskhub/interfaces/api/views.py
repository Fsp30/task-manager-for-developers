from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from requests_oauthlib import OAuth2Session

def github_login(request):
    github = OAuth2Session(
        settings.GITHUB_CLIENT_ID,
        redirect_uri=settings.GITHUB_CALLBACK_URL,
        scope=['read:user', 'user:email']
    )
    auth_url, state = github.authorization_url('https://github.com/login/oauth/authorize')
    request.session['oauth_state'] = state
    return redirect(auth_url)

def github_callback(request):
    github = OAuth2Session(
        settings.GITHUB_CLIENT_ID,
        state=request.session.get('oauth_state'),
        redirect_uri=settings.GITHUB_CALLBACK_URL
    )
    token = github.fetch_token(
        'https://github.com/login/oauth/access_token',
        client_secret=settings.GITHUB_CLIENT_SECRET,
        code=request.GET.get('code')
    )
    user_data = github.get('https://api.github.com/user').json()
    request.session['user_data'] = {
        'login': user_data.get('login'),
        'token': token.get('access_token')
    }

    return redirect('/')

def home(request):
    user_data = request.session.get('user_data')
    return render(request, 'home.html', {'user_data': user_data})

def logout_view(request):
    request.session.flush()
    return redirect('/')
