from django.contrib import admin
from .models import Task

@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'completed', 'user', 'repeat', 'due_date')
    list_filter = ('completed', 'user')
    search_fields = ('title', 'description')