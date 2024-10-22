from django.urls import path
from .views import (
    register,
    login_view,
    logout_view,
    create_project,
    get_projects,
    create_task,
    get_tasks,
    task_detail,
    create_worker,
    get_workers,
    worker_detail,
)

urlpatterns = [
    path('api/register/', register, name='register'),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
    
    # Project URLs
    path('api/projects/', create_project, name='create_project'),
    path('api/projects/list/', get_projects, name='get_projects'),
    
    # Task URLs
    path('api/tasks/', create_task, name='create_task'),
    path('api/tasks/list/', get_tasks, name='get_tasks'),
    path('api/tasks/<int:pk>/', task_detail, name='task_detail'),
    
    # Worker URLs
    path('api/workers/', create_worker, name='create_worker'),  # Create a new worker
    path('api/workers/list/', get_workers, name='get_workers'),  # List all workers
    path('api/workers/<int:pk>/', worker_detail, name='worker_detail'),  # Retrieve, update, or delete a worker
]

