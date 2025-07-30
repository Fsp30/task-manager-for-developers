
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
from taskhub.interfaces.api.views.note_views import NoteViewSet
from taskhub.interfaces.api.views.enterprise_views import EnterpriseViewSet
from taskhub.interfaces.api.views.repository_views import RepositoryViewSet
from taskhub.interfaces.api.views.contentRepository_views import ContentRepositoryViewSet
from taskhub.interfaces.api.views.repositoryPermission_views import RepositoryPermissionViewSet 
from taskhub.interfaces.api.views.user_views import UserViewSet 


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'notes', NoteViewSet, basename='notes')
router.register(r'enterprise', EnterpriseViewSet, basename='enterprise')
router.register(r'repository', RepositoryViewSet, basename='repository')
router.register(r'content_repository', ContentRepositoryViewSet, basename='content_repository')
router.register(r'repository_permission', RepositoryPermissionViewSet, basename='repository_permission')
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin2/', site.urls),
    # path('auth/login/', views.github_login, name='github_login'),
    # path('auth/callback/', views.github_callback, name='github_callback'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)), 
]

 