from django.contrib import admin
from .models import Project, Task, Manager, Supervisor, Worker  # Import Worker model

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'budget', 'timeline', 'supervisor')  # Added supervisor to display
    search_fields = ('name', 'location')
    list_filter = ('timeline', 'supervisor')  # Added supervisor for filtering

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date')
    search_fields = ('title', 'project__name')
    list_filter = ('due_date',)

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')

class SupervisorAdmin(admin.ModelAdmin):  # New SupervisorAdmin class
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')

class WorkerAdmin(admin.ModelAdmin):  # New WorkerAdmin class
    list_display = ('name', 'token_no', 'is_available')  # Fields to display
    search_fields = ('name', 'token_no')  # Fields to search
    list_filter = ('is_available',)  # Filter by availability

# Registering models with the admin site
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Supervisor, SupervisorAdmin)  # Register the Supervisor model
admin.site.register(Worker, WorkerAdmin)  # Register the Worker model
