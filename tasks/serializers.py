from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'completed', 'repeat', 'description', 'created_at', 'user', 'due_date'
            ]
        read_only_fields = ['user']
        