from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'completed', 'user')
    list_filter = ('completed', 'user')
    search_fields = ('title', 'description')