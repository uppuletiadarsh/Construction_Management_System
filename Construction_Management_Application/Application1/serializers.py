from rest_framework import serializers
from .models import Supervisor, Manager, Project, Worker, Task
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import User, Manager, Supervisor




class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[('manager', 'Manager'), ('supervisor', 'Supervisor')])
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    mobile_number = serializers.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'name', 'email', 'mobile_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        name = validated_data.pop('name')
        email = validated_data.pop('email')
        mobile_number = validated_data.pop('mobile_number')

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        if role == 'manager':
            Manager.objects.create(user=user, name=name, email=email, mobile_number=mobile_number)
        elif role == 'supervisor':
            Supervisor.objects.create(user=user, name=name, email=email, mobile_number=mobile_number)

        return user



from rest_framework import serializers
from .models import Supervisor, Manager, Project, Worker, Task

class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ['id', 'user', 'name', 'email', 'mobile_number']

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'user', 'name', 'email', 'mobile_number']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'location', 'budget', 'timeline', 'supervisor']

from rest_framework import serializers
from .models import Task, Worker

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'name', 'token_no', 'is_available']  # Adjust as needed
from rest_framework import serializers
from .models import Task, Worker

from rest_framework import serializers
from .models import Task, Worker

class TaskSerializer(serializers.ModelSerializer):
    workers = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'project', 'image', 'workers']

    def create(self, validated_data):
        workers_token_no = validated_data.pop('workers', [])
        
        # Check for availability of each worker by token_no
        unavailable_workers = []
        workers = []

        for token in workers_token_no:
            try:
                worker = Worker.objects.get(token_no=token)
                if not worker.is_available:
                    unavailable_workers.append(worker.name)
                else:
                    workers.append(worker)
            except Worker.DoesNotExist:
                unavailable_workers.append(f"Worker with token number {token} does not exist.")

        if unavailable_workers:
            raise serializers.ValidationError(f"The following workers are not available: {', '.join(unavailable_workers)}")

        # Create the task and assign available workers
        task = Task.objects.create(**validated_data)
        task.workers.set(workers)  # Set workers using the Worker objects
        return task

    def update(self, instance, validated_data):
        workers_token_no = validated_data.pop('workers', [])
        
        # Check for availability of each worker by token_no
        unavailable_workers = []
        workers = []

        for token in workers_token_no:
            try:
                worker = Worker.objects.get(token_no=token)
                if not worker.is_available:
                    unavailable_workers.append(worker.name)
                else:
                    workers.append(worker)
            except Worker.DoesNotExist:
                unavailable_workers.append(f"Worker with token number {token} does not exist.")

        if unavailable_workers:
            raise serializers.ValidationError(f"The following workers are not available: {', '.join(unavailable_workers)}")

        # Update task details and workers
        instance = super().update(instance, validated_data)
        instance.workers.set(workers)
        return instance
