from django.urls import path
from .views import (
    register,
    login_view,
    logout_view,
    my_profile,
    create_project,
    get_projects,
    create_task,
    get_tasks,
    task_detail,
    get_workers,
    create_worker,
    worker_detail,
    get_resources,
    create_resource,
    resource_detail,
    put_or_delete_project,
    manage_supervisor,
    #manager_dashboard,
    get_supervisors,
    

)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('myprofile/', my_profile, name='my_profile'),
    path('projects/', get_projects, name='get_projects'),
    path('projects/create/', create_project, name='create_project'),
    path('tasks/', get_tasks, name='get_tasks'),
    path('supervisors/<int:pk>/', manage_supervisor, name='manage_supervisor'),
    path('projects/<int:pk>/', put_or_delete_project, name='put_or_delete_project'), 
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
    path('workers/', get_workers, name='get_workers'),
    path('workers/create/', create_worker, name='create_worker'),
    path('workers/<int:pk>/', worker_detail, name='worker_detail'),
    path('resources/', get_resources, name='get_resources'),  
    path('resources/create/', create_resource, name='create_resource'),  
    path('resources/<int:pk>/', resource_detail, name='resource_detail'),  
    path('manager/tasks/', get_tasks, name='get_tasks'),
    path('manager/workers/', get_workers, name='get_workers'),
    path('manager/resources/', get_resources, name='get_resources'),
    path('manager/supervisors/', get_supervisors, name='get_supervisors'),
]
