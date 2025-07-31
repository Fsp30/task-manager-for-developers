from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from requests_oauthlib import OAuth2Session
from rest_framework_simplejwt.tokens import RefreshToken
from taskhub.core.models.user import User
from taskhub.utils.jwt import generate_custom_jwt

def github_login(request):
    github = OAuth2Session(
        client_id=settings.GITHUB_CLIENT_ID,
        redirect_uri=settings.GITHUB_CALLBACK_URL,
        scope=['read:user', 'user:email']
    )
    auth_url, state = github.authorization_url('https://github.com/login/oauth/authorize')
    request.session['oauth_state'] = state
    return redirect(auth_url)

def github_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Código de autorização não fornecido pelo GitHub'}, status=400)

    github = OAuth2Session(
        client_id=settings.GITHUB_CLIENT_ID,
        state=request.session.get('oauth_state'),
        redirect_uri=settings.GITHUB_CALLBACK_URL
    )

    token = github.fetch_token(
        'https://github.com/login/oauth/access_token',
        client_secret=settings.GITHUB_CLIENT_SECRET,
        code=code
    )

    user_data = github.get('https://api.github.com/user').json()
    email_data = github.get('https://api.github.com/user/emails').json()
    email = next((e["email"] for e in email_data if e.get("primary")), None)

    git_id = user_data.get('login')
    user = User.objects(gitId=git_id).first()

    if not user:
        user = User(
            gitId=git_id,
            email=email or f'{git_id}@users.noreply.github.com',
            userName=user_data.get('name') or git_id
        )
        user.save()

   
    jwt_custon_refresh = generate_custom_jwt(user)

    request.session['user_data'] = {
        'login': git_id,
        'github_token': token.get('access_token'),
        'jwt': jwt_custon_refresh,
    }

    return redirect('/')

def home(request):
    user_data = request.session.get('user_data')
    return render(request, 'home.html', {'user_data': user_data})

def logout_view(request):
    request.session.flush()
    return redirect('/')
