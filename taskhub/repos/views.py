from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("""
        <h1>Test dev's</h1>
        <a href='/auth/login/github/'>
            <button>Login com GitHub</button>
        </a>
    """)
