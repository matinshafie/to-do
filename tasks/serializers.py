from rest_framework import serializers
from .models import Task, List
from django.utils import timezone


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'completed', 'completed_at', 'list']

    def create(self, validated_data:dict):
        repeat = validated_data.get('repeat')
        due_date = validated_data.get('due_date')

        if repeat and not due_date:
            validated_data['due_date'] = timezone.now().date()

        return super().create(validated_data)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'completed_at', 'list']

class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'repeat', 'due_date', 'list']
        read_only_fields = ['list']

    def update(self, instance: Task, validated_data: dict):
        completed = validated_data.get('completed', instance.completed)
        repeat = validated_data.get('repeat', instance.repeat)

        if completed and repeat:
            if not validated_data.get('due_date'):
                validated_data['due_date'] = timezone.now().date()
            validated_data['due_date'] += timezone.timedelta(days=repeat)
            validated_data['completed'] = False

        return super().update(instance, validated_data)



class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'title']