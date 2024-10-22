from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Manager, Supervisor, Project, Task, Worker
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, WorkerSerializer
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
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_projects(request):
    """Get a list of projects (Managers only)."""
    if not hasattr(request.user, 'manager'):
        return Response({'message': 'You do not have permission to view projects.'}, status=status.HTTP_403_FORBIDDEN)

    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_task(request):
    """Create a new task (Supervisors only)."""
    if not hasattr(request.user, 'supervisor'):
        return Response({'message': 'You do not have permission to create a task.'}, status=status.HTTP_403_FORBIDDEN)

    print("Request data:", request.data)  # Debug print
    serializer = TaskSerializer(data=request.data)
    
    if serializer.is_valid():
        print("Valid data:", serializer.validated_data)  # Debug print
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print("Errors:", serializer.errors)  # Debug print
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_tasks(request):
    """Get a list of tasks (Managers can view, Supervisors can modify)."""
    tasks = Task.objects.all()  # All users can see tasks
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def task_detail(request, pk):
    """Retrieve, update, or delete a task."""
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check permissions based on user role
    if hasattr(request.user, 'supervisor'):
        # Supervisors can perform all actions
        if request.method == 'GET':
            serializer = TaskSerializer(task)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    elif hasattr(request.user, 'manager'):
        # Managers can only view the task details
        if request.method == 'GET':
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        else:
            return Response({'message': 'You do not have permission to modify this task.'}, status=status.HTTP_403_FORBIDDEN)

    return Response({'message': 'You do not have permission to view this task.'}, status=status.HTTP_403_FORBIDDEN)

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
        return Response(status=status.HTTP_404_NOT_FOUND)

    if hasattr(request.user, 'supervisor'):
        # Supervisors can perform all actions
        if request.method == 'GET':
            serializer = WorkerSerializer(worker)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = WorkerSerializer(worker, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            worker.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({'message': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)



