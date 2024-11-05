from django.db import models
from django.contrib.auth.models import User


# Supervisor Model
class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Add name field
    email = models.EmailField(max_length=254)  # Add email field
    mobile_number = models.CharField(max_length=15)  # Add mobile number field

    def __str__(self):
        return self.name  # You can also return user.username if preferred

# Manager Model
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Add name field
    email = models.EmailField(max_length=254)  # Add email field
    mobile_number = models.CharField(max_length=15)  # Add mobile number field

    def __str__(self):
        return self.name  # You can also return user.username if preferred

# Project Model
class Project(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    timeline = models.DateField()
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# Worker Model
class Worker(models.Model):
    name = models.CharField(max_length=100)
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    timeline = models.DateField()
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# Worker Model
class Worker(models.Model):
    name = models.CharField(max_length=100)
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Task Model
from django.db import models

from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Worker(models.Model):
    name = models.CharField(max_length=100)
    token_no = models.CharField(max_length=50, unique=True)  # Ensure token number is unique
    is_available = models.BooleanField(default=True)  # Availability status

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='task_images/', null=True, blank=True)  # Image field
    workers = models.ManyToManyField(Worker, blank=True)  # Many-to-many relationship with Worker

    def __str__(self):
        return self.title



