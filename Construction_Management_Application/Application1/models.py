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






class Project(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    timeline = models.DateField()
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


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



class Resource(models.Model):
    RESOURCE_TYPES = [
        ('material', 'Material'),
        ('equipment', 'Equipment'),
        ('labor', 'Labor'),
    ]
    
    resource_name = models.CharField(max_length=100)  # Resource name (e.g., concrete, scaffolding)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)  # Type of resource
    quantity = models.PositiveIntegerField()  # Available quantity
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Link to project

    def __str__(self):
        return f"{self.resource_name} ({self.resource_type})"
    

   

"""
class TaskMedia(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='media_files')  # Link to the Task
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)  # To store whether it's an image or a video
    media_file = models.FileField(upload_to='task_media/')  # Field to store the media file (image/video)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the media is uploaded

    def __str__(self):
        return f"{self.get_media_type_display()} for Task: {self.task.title}"
    class Meta:
        verbose_name = 'Task Media'
        verbose_name_plural = 'Task Media Files'"""
