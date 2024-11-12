from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Manager, Supervisor, Project, Task, Worker
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, WorkerSerializer, SupervisorSerializer, ManagerSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def register(request):
    """Register a new Manager or Supervisor."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'User created', 'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_view(request):
    """Login a user."""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login successful', 'token': token.key})
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout a user."""
    logout(request)
    return Response({'message': 'Logout successful'})



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_profile(request):
    """Get the logged-in user's profile details."""
    user_data = {
        "username": request.user.username,
        "email": request.user.email,  # Ensure user email is available
    }

    if hasattr(request.user, 'manager'):
        manager = request.user.manager
        serializer = ManagerSerializer(manager)
        return Response({**user_data, **serializer.data})  # Combine user and manager data

    elif hasattr(request.user, 'supervisor'):
        supervisor = request.user.supervisor
        serializer = SupervisorSerializer(supervisor)
        return Response({**user_data, **serializer.data})  # Combine user and supervisor data

    return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_project(request):
    """Create a new project (Managers only)."""
    if not hasattr(request.user, 'manager'):
        return Response({'message': 'You do not have permission to create a project.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



from rest_framework.decorators import api_view, permission_classes

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def put_or_delete_project(request, pk):
    """Update or delete an existing project (Managers only)."""
    try:
        # Retrieve the project by primary key (pk)
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({'message': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the logged-in user is a manager
    if not hasattr(request.user, 'manager'):
        return Response({'message': 'You do not have permission to modify this project.'}, status=status.HTTP_403_FORBIDDEN)
    # Handle PUT request for updating the project
    if request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Handle DELETE request for deleting the project
    elif request.method == 'DELETE':
        project.delete()
        return Response({'message': 'Project deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_projects(request):
    """Get a list of projects (Managers only)."""
    if not hasattr(request.user, 'manager'):
        return Response({'message': 'You do not have permission to view projects.'}, status=status.HTTP_403_FORBIDDEN)

    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_supervisor(request, pk):
    """Get, update, or delete a supervisor (Managers only for PUT and DELETE)."""
    try:
        # Retrieve the supervisor by primary key (pk)
        supervisor = Supervisor.objects.get(pk=pk)
    except Supervisor.DoesNotExist:
        return Response({'message': 'Supervisor not found.'}, status=status.HTTP_404_NOT_FOUND)
    # Check if the logged-in user is a manager
    if not hasattr(request.user, 'manager'):
        return Response({'message': 'You do not have permission to modify this supervisor.'}, status=status.HTTP_403_FORBIDDEN)
    # Handle GET request (any authenticated user can view the supervisor)
    if request.method == 'GET':
        serializer = SupervisorSerializer(supervisor)
        return Response(serializer.data)
    # Handle PUT request (only manager can update the supervisor)
    elif request.method == 'PUT':
        serializer = SupervisorSerializer(supervisor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Handle DELETE request (only manager can delete the supervisor)
    elif request.method == 'DELETE':
        supervisor.delete()
        return Response({'message': 'Supervisor deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_task(request):
    """Create a new task (Supervisors only)."""
    if not hasattr(request.user, 'supervisor'):
        return Response({'message': 'You do not have permission to create a task.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_tasks(request):
    """Get a list of tasks (All users can see tasks)."""
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def task_detail(request, pk):
    """Retrieve, update, or delete a task."""
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'message': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
    if hasattr(request.user, 'supervisor'):
        # Supervisors can perform all actions
        if request.method == 'GET':
            # Retrieve task details
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        elif request.method == 'PUT':
            # Update task details
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()  # Save the updated task
                return Response({
                    'message': 'Task updated successfully.',
                    'task': serializer.data  # Returning the updated task details
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            # Delete the task
            task.delete()
            return Response({
                'message': 'Task deleted successfully.'
            }, status=status.HTTP_204_NO_CONTENT)

    # If the user does not have supervisor permissions
    return Response({
        'message': 'You do not have permission to perform this action.'
    }, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_workers(request):
    """Get a list of workers (Supervisors only)."""
    if not hasattr(request.user, 'supervisor'):
        return Response({'message': 'You do not have permission to view workers.'}, status=status.HTTP_403_FORBIDDEN)

    workers = Worker.objects.all()
    serializer = WorkerSerializer(workers, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_worker(request):
    """Create a new worker (Supervisors only)."""
    if not hasattr(request.user, 'supervisor'):
        return Response({'message': 'You do not have permission to create a worker.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = WorkerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def worker_detail(request, pk):
    """Retrieve, update, or delete a worker."""
    try:
        worker = Worker.objects.get(pk=pk)
    except Worker.DoesNotExist:
        return Response({'message': 'Worker not found.'}, status=status.HTTP_404_NOT_FOUND)
    if hasattr(request.user, 'supervisor'):
        # Supervisors can perform all actions
        if request.method == 'GET':
            serializer = WorkerSerializer(worker)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = WorkerSerializer(worker, data=request.data)
            if serializer.is_valid():
                # Save the modified worker details
                serializer.save()
                return Response({'message': 'Worker updated successfully.', 'worker': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            worker.delete()
            return Response({'message': 'Worker deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    # If the user is not a supervisor, deny access
    return Response({'message': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)



from .models import Resource
from .serializers import ResourceSerializer
# Custom permission for Supervisor only actions
class IsSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'supervisor')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_resources(request):
    """View resources (Managers only)."""
    if hasattr(request.user, 'manager'):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)
    return Response({'message': 'You do not have permission to view resources.'}, status=status.HTTP_403_FORBIDDEN)



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSupervisor])
def create_resource(request):
    """Create a new resource (Supervisors only)."""
    serializer = ResourceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsSupervisor])
def resource_detail(request, pk):
    """Retrieve, update, or delete a resource (Supervisors only)."""
    try:
        resource = Resource.objects.get(pk=pk)
    except Resource.DoesNotExist:
        return Response({'message': 'Resource not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ResourceSerializer(resource)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ResourceSerializer(resource, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Resource updated successfully.',
                'resource': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        resource.delete()
        return Response({
            'message': 'Resource deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)




"""@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_dashboard(request):
     #Get tasks, workers, resources, and supervisors for managers.
    # Ensure the user is a manager
    if not hasattr(request.user, 'manager'):
        return Response({'message': 'You do not have permission to access this information.'}, status=status.HTTP_403_FORBIDDEN)

    # Retrieve all relevant data
    tasks = Task.objects.all()
    workers = Worker.objects.all()
    resources = Resource.objects.all()
    supervisors = Supervisor.objects.all()

    # Serialize the data
    task_serializer = TaskSerializer(tasks, many=True)
    worker_serializer = WorkerSerializer(workers, many=True)
    resource_serializer = ResourceSerializer(resources, many=True)
    supervisor_serializer = SupervisorSerializer(supervisors, many=True)
    # Prepare a combined response
    response_data = {
        'tasks': task_serializer.data,
        'workers': worker_serializer.data,
        'resources': resource_serializer.data,
        'supervisors': supervisor_serializer.data,
    }
    response_data['message'] = 'Data successfully retrieved for the manager.'

    return Response(response_data, status=status.HTTP_200_OK)"""

# Helper function to check if the user is a manager
def is_manager(user):
    try:
        return hasattr(user, 'manager')
    except Manager.DoesNotExist:
        return False


# Tasks View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    """Get all tasks for managers."""
    if not is_manager(request.user):
        return Response({'message': 'You do not have permission to access this information.'}, status=status.HTTP_403_FORBIDDEN)

    tasks = Task.objects.all()
    task_serializer = TaskSerializer(tasks, many=True)
    return Response({
        'tasks': task_serializer.data,
        'message': 'Tasks successfully retrieved for the manager.'
    }, status=status.HTTP_200_OK)


# Workers View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workers(request):
    """Get all workers for managers."""
    if not is_manager(request.user):
        return Response({'message': 'You do not permission to access this information.'}, status=status.HTTP_403_FORBIDDEN)

    workers = Worker.objects.all()
    worker_serializer = WorkerSerializer(workers, many=True)
    return Response({
        'workers': worker_serializer.data,
        'message': 'Workers successfully retrieved for the manager.'
    }, status=status.HTTP_200_OK)


# Resources View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_resources(request):
    """Get all resources for managers."""
    if not is_manager(request.user):
        return Response({'message': 'You do not have permission to access this information.'}, status=status.HTTP_403_FORBIDDEN)

    resources = Resource.objects.all()
    resource_serializer = ResourceSerializer(resources, many=True)
    return Response({
        'resources': resource_serializer.data,
        'message': 'Resources successfully retrieved for the manager.'
    }, status=status.HTTP_200_OK)


# Supervisors View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_supervisors(request):
    """Get all supervisors for managers."""
    if not is_manager(request.user):
        return Response({'message': 'You do not have permission to access this information.'}, status=status.HTTP_403_FORBIDDEN)

    supervisors = Supervisor.objects.all()
    supervisor_serializer = SupervisorSerializer(supervisors, many=True)
    return Response({
        'supervisors': supervisor_serializer.data,
        'message': 'Supervisors successfully retrieved for the manager.'
    }, status=status.HTTP_200_OK)
