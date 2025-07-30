from django.contrib import admin
from django.urls import path, include
from django_mongoengine.mongo_admin.sites import site as mongo_admin_site
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.routers import DefaultRouter
from taskhub.interfaces.api.views import (
    task_views,
    note_views,
    enterprise_views,
    repository_views,
    contentRepository_views,
    repositoryPermission_views,
    user_views
)
from . import views_main


router = DefaultRouter()
router.register(r'tasks', task_views.TaskViewSet, basename='task')
router.register(r'notes', note_views.NoteViewSet, basename='notes')
router.register(r'enterprise', enterprise_views.EnterpriseViewSet, basename='enterprise')
router.register(r'repository', repository_views.RepositoryViewSet, basename='repository')
router.register(r'content_repository', contentRepository_views.ContentRepositoryViewSet, basename='content_repository')
router.register(r'repository_permission', repositoryPermission_views.RepositoryPermissionViewSet, basename='repository_permission')
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mongo-admin/', mongo_admin_site.urls),
    path('auth/login/', views_main.github_login, name='github_login'),
    path('auth/callback/', views_main.github_callback, name='github_callback'),
    path('auth/logout/', views_main.logout_view, name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('', views_main.home, name='home'),
]
