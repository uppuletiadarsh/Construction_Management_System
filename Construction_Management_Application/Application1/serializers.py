from rest_framework import serializers
from .models import Supervisor, Manager, Project, Worker, Task
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import User, Manager, Supervisor

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Manager, Supervisor
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Manager, Supervisor

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

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'name', 'skill']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'project', 'worker']

