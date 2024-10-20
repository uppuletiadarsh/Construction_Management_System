from django.urls import path
from .views import register, login_view, logout_view, create_project, create_task

urlpatterns = [
    path('api/register/', register, name='register'),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
    path('api/projects/', create_project, name='create_project'),
    path('api/tasks/', create_task, name='create_task'),
]
