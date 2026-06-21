from rest_framework import serializers
from .models import Task
from django.utils import timezone


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'completed', 'completed_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'completed_at']

class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'repeat', 'due_date', 'list']

    def update(self, instance: Task, validated_data: dict):
        completed = validated_data.get('completed', instance.completed)
        repeat = validated_data.get('repeat', instance.repeat)

        if completed and repeat:
            validated_data['due_date'] += timezone.timedelta(days=repeat)
            validated_data['completed'] = False

        return super().update(instance, validated_data)
