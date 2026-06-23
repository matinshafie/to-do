from django.db import models
from django.conf import settings
from uuid import uuid4


class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lists'
        )
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks'
        )
    repeat = models.PositiveIntegerField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    list = models.ForeignKey(List, models.CASCADE, related_name='tasks', blank=True, null=True)

class CompletedTask(models.Model):
    tasks = models.ForeignKey(Task, models.CASCADE, related_name='completed_tasks')
    completed_at = models.DateTimeField(auto_now_add=True)