
from django.contrib import admin
from django.urls import path, include
from django_mongoengine.mongo_admin.sites import site
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.routers import DefaultRouter
from taskhub.interfaces.api.views.task_views import TaskViewSet

# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin2/', site.urls),
    # path('auth/login/', views.github_login, name='github_login'),
    # path('auth/callback/', views.github_callback, name='github_callback'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/', include(router.urls)), 
]

 