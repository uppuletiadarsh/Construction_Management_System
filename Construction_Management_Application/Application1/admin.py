from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, Task, Manager

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'budget', 'timeline')
    search_fields = ('name', 'location')
    list_filter = ('timeline',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date')
    search_fields = ('title', 'project__name')
    list_filter = ('due_date',)

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')

# Registering models with the admin site
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Manager, ManagerAdmin)